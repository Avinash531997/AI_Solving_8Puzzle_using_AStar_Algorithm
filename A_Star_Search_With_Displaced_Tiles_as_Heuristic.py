import sys
import copy
import time
 
#The input and the goal states are passed through an input file .

with open('input.txt', 'r') as input_file:
    data_item = [[int(num) for num in line.split()] for line in input_file if line.strip() != ""]

#Extracting the Input and Goal States from the input file.

start_state = data_item[0:3].copy()
goal_state = data_item[3:6].copy()

termination_time = 3600 # Termination time in seconds of program if the solution is not obtained within the timit limit


#Defining the structure of the node.
class node:
    
    def __init__(self,starts = None,d = None,path = None,move = None,h = None):
        self.state = starts
        self.depth = d
        self.hvalue = h
        self.curPath = path
        self.operation = move
    
    def display(self,tlist):       
        for i in range(0,3):
                print(tlist[i])
            
    
    #Finding the neighbors/Children of the current node.
    def generate_sub_space(self,parent,visited,h = None,total_nodes = None):
        children = []
        x = None
        y = None
        
        
        #Finding the Position of Blank Space
        for i in range(0,3):
            for j in range(0,3):
                if parent.state[i][j] == 0 :
                    x=i
                    y=j
                    break
                
            if x is not None:
                break
         
        #Defining actions on all possible moves of the Blank space.
        if x != 0:
            tpath = copy.deepcopy(parent.curPath)
            tpath.append("Up")
            child = node(copy.deepcopy(parent.state),parent.depth + 1,tpath,"Up",h)
            child.state[x - 1][y],child.state[x][y] = child.state[x][y],child.state[x - 1][y]
            if self.to_String(child.state) not in visited:
                children.append(child)
                total_nodes = total_nodes + 1   
        
        if x != 2:
            tpath = copy.deepcopy(parent.curPath)
            tpath.append("Down")
            child = node(copy.deepcopy(parent.state),parent.depth + 1,tpath,"Down",h)
            child.state[x + 1][y],child.state[x][y] = child.state[x][y],child.state[x + 1][y]
            if self.to_String(child.state) not in visited:
                children.append(child)
                total_nodes = total_nodes + 1           
        
        if y != 0:
            tpath = copy.deepcopy(parent.curPath)
            tpath.append("Left")
            child = node(copy.deepcopy(parent.state),parent.depth + 1,tpath,"Left",h)
            child.state[x][y - 1],child.state[x][y] = child.state[x][y],child.state[x][y - 1]
            if self.to_String(child.state) not in visited:
                children.append(child)
                total_nodes = total_nodes + 1
       
        if y != 2:
            tpath = copy.deepcopy(parent.curPath)
            tpath.append("Right")
            child = node(copy.deepcopy(parent.state),parent.depth + 1,tpath,"Right",h)
            child.state[x][y + 1],child.state[x][y] = child.state[x][y],child.state[x][y + 1]
            if self.to_String(child.state) not in visited:
                children.append(child)
                total_nodes = total_nodes + 1     
        
        return children,total_nodes #Returning all possible children of the current node       
        
    def to_String(self,temp_state):
        s=''
        for i in temp_state:
            for j in i:
                s = s + str(j)
        return s
    
    #Calculating displaced tile heuristic value
    def heuristic_displacedTiles(self,state):
        score=0
        for i in range(0,3):
            for j in range(0,3):
                if (state[i][j] != 0):
                    if(state[i][j]!=goal_state[i][j]):
                        score+=1
        return score
     
    #Astar using Dispalced tile heuristic
    def A_Star_Search_With_Displaced_Tiles_as_Heuristic(self):
        max_list_size=-sys.maxsize-1
        total_nodes=0
        time_flag=0
        start_time = time.time()
        queue=[]
        flag=0
        visited = set()
        start_node = node(start_state, 1, [],'',self.heuristic_displacedTiles(start_state))
        queue.append(start_node)
        while(queue):
            if len(queue)>max_list_size:
                max_list_size=len(queue)
            temp_time = time.time()
            if (temp_time - start_time >= termination_time):
                time_flag = 1
                break
            queue.sort(key=lambda x: x.hvalue) #Sorting the child nodes stored in the queue based on their heuristic value.
            current_node= queue.pop(0)
            state_string = self.to_String(current_node.state)
            visited.add(state_string)
            if (current_node.state == goal_state):
                
                print("Moves="+str(len(current_node.curPath)))
                print(str(current_node.curPath))
                flag = 1
                print('')
                print("Total Nodes Visited=" + str(total_nodes))
                print("A* with Out of Place Heuristic Time"+ str(time.time()-start_time))
                print("Maximum List Size="+str(max_list_size))

            if flag == 1:
                break
            tchilds,total_nodes=self.generate_sub_space(current_node,visited,current_node.depth+self.heuristic_displacedTiles(current_node.state),total_nodes)
            queue.extend(tchilds)# Adding the expanded chidrens to the list
			
        if time_flag == 1:
            print("Failure, The program is not able to give solution within the time limit")
            print("Total Nodes Visited=" + str(total_nodes))
            print("A* with Out of Place Heuristic terminated due to time out in "+str(int(time.time()-start_time)/60)+" minutes")    
              
if __name__ == "__main__":
    obj1=node()
    print("\n Start State is : ")
    obj1.display(start_state)
    
    print("\n Goal State is : ")
    obj1.display(goal_state)
    obj1.A_Star_Search_With_Displaced_Tiles_as_Heuristic()
            