from board import Board, PIECE_MAPPING


"""
class RL - reinforcement learning using Q learning values

@:var start {(int, int)} starting position of piece
@:var target: {(int, int)} target square that piece can move to
@:var capture: {bool} is it a capture move
"""
LEARNING_RATE=0.1
DISCOUNT_FACTOR=0.4

class RL:
    def __init__(self, model):
        self.model=model

    def compute_move(self,board, reward,minmaxmove):
        curr_state=board.str_positions()

        QSA=0
        QSAN=[]
        all_valid_moves=[]
        all_valid_states=[]  
        for rank in range(1, 10+1):
            for file in range(1, 9+1):
                valid_moves_arr=board.generateValidMoves(file,rank)    
                #print(valid_moves_arr)
                for m in valid_moves_arr:        
                    sim_b=board.simulateMove(m)
                    #print(sim_b)
                    sim_state=board.str_positions_board(sim_b)
                    #print(sim_state)
                    all_valid_states.append(sim_state)
                    all_valid_moves.append(m)
                    #print(m)
        #print(all_valid_states)
        #print(len(all_valid_moves))
        
        #find value QSA if it does not exist, creat a new entry in dictionary and assignt it vallue 0
        if self.model.get(curr_state) is not None:
            QSA=self.model[curr_state]
        else:
            self.model.setdefault(curr_state, -20)
            QSA=-20

        for sim in all_valid_states:
            #print(sim)
            
            if self.model.get(sim) is not None:

                QSAN.append(self.model[sim])
            else:
                self.model.setdefault(sim, -20)
                QSAN.append(-20)
                
        
        QSA_opt=max(QSAN)
        if QSA_opt<=reward: #for the beginning of learning 
            best_Q_move=minmaxmove
            sim_b=board.simulateMove(minmaxmove)
            sim_state=board.str_positions_board(sim_b)
            QSA=self.model[sim_state]
            QSA=QSA+ LEARNING_RATE*(reward+ DISCOUNT_FACTOR*(QSA_opt-QSA))
            self.model[sim_state]=QSA

        else:
            #print(QSAN)
            ixd_opt=QSAN.index(QSA_opt)
            best_Q_move=all_valid_moves[ixd_opt]
            #print("asd",best_Q_move)
            QSA=self.model[all_valid_states[ixd_opt]]
            QSA=QSA+ LEARNING_RATE*(reward+ DISCOUNT_FACTOR*(QSA_opt-QSA))
            self.model[all_valid_states[ixd_opt]]=QSA

        return best_Q_move, QSA

    def return_model(self):
        return self.model

    #original model is trained for computer=w, if computer plays as black sign of values has to be changed 
    def revert_model(self): 
        for key in self.model:
            self.model[key] = -self.model[key]