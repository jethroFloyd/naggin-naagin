#!/usr/bin/env python

# Heavily Modified.


import interact
import snake_game.directions

import sys

def DynamicImportMember(classpath):
  """ Imports a variable (function/class) dynamically, given its class path.
  For example, given state_mappers.quadrant_view.QuadrantView this function
  does
        from state_mappers.quadrant_view import quadrant_view
        return quadrant_view.QuadrantView """
  try:
    module_name, variable_name = classpath.rsplit('.', 1)
    module = __import__(module_name, fromlist = module_name)
    return module.__dict__[variable_name]
  except ImportError, e:
    sys.stderr.write("Import %s failed \n"%(classpath))
    sys.stderr.write(str(e) + "\n")
    sys.exit(1)
  except KeyError, e:
    sys.stderr.write("Module %s does not contain %s \n"%(
      module_name, variable_name))
    sys.stderr.write(str(e) + "\n")
    sys.exit(1)
  return None



class AgentInteract(interact.Interact):
  """ Interacts with a specified RL agent which is initialised using a given
  state_mapper. The agent uses the state mapper to map the state passed to it.

      This interactor also makes the agent backup its knowledge every so many
      moves."""
  def __init__(self, agent_string, state_mapper_string, 
      trained_filename, dump_filename, backup_num_moves = 100):
    self.trained_filename = trained_filename
    self.dump_filename = dump_filename

    self.state_mapper_class = DynamicImportMember(state_mapper_string)
    self.agent_class = DynamicImportMember(agent_string)

    self.agent = self.agent_class(self.trained_filename)
    self.state_mapper = self.state_mapper_class(snake_game.directions)

    self.move_counter = 0
    self.backup_num_moves = backup_num_moves

    self.episode_ended = False
    self.reward = 0
    return


# Here we formally write the reward matrix for the Q Learning.
# If the snake makes a move (self.move_counter++); we have a penalty
# of 1 if it does nothing, a penalty of 1000 if it dies and
# a penalty of 50 if it eats the fruit.

# Why 50, 1000 and 1? Trial and Error.

  def PerformAndReturnNextMove(self, sl):
    self.move_counter += 1

    if self.move_counter == self.backup_num_moves:
      self.agent.WriteKnowledge(self.dump_filename)
      self.move_counter = 0

    state_ = self.state_mapper.TransformState(sl)
    move_ = self.agent.Act(state_, self.state_mapper.GetAllowedMoves(sl),
        self.reward, self.episode_ended)
    # reverse_direction = snake_game.directions.Reverse(sl.state.direction)
    move = self.state_mapper.TransformMove(sl, move_)

    # Make the move
    sl.Move(move)

    # If nothing happens
    self.reward = -1

    # Handle the case we died
    if not sl.IsAlive():
      self.reward = -1000
      self.episode_ended = True
      # print "Episode Ended"
      print "E"
    else:
      self.episode_ended = False

    # If we ate a fruit
    if sl.WasFruitEaten():
      self.reward = 300
      print "F"
    
    # If the bot made the reverse direction move.
    # if move == reverse_direction:
    #  self.reward -= 1
    print "M"
    return move
