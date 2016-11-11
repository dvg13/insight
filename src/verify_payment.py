import sys
import copy

#class to represent the connection graph
#each node (where a node is an item in a dict) holds an edge list which is represented as a set
class Payment_Graph():
    def __init__ (self):
        self.connections = {}

    #add a connection to the graph (really two connections as it's undirected)
    def add_connection(self,id_1,id_2):

        #update id_1
        if id_1 not in self.connections:
            self.connections[id_1] = set()
        self.connections[id_1].add(id_2)

        #update id_2
        if id_2 not in self.connections:
            self.connections[id_2] = set()
        self.connections[id_2].add(id_1)

    #determine whether the two id's are withing some number of degrees of each other
    #basic approach is to start from each end - the reduces the size of the candidates set
    #this size will be number_of_connections ^ k
    #so 2 * n^k/2 is probably smaller than n^k.  
    def in_network(self,id_1,id_2,degree):
        #if either id is not in the graph - then they aren't in the same network
        if id_1 not in self.connections or id_2 not in self.connections:
            return False
       
        #initially the candidate is just that id
        ids_from_1 = {id_1}
        ids_from_2 = {id_2}

      
        #advance both candidates lists, test for intersection at the end
        #it's always better to expand the shorter set
        #this also tests the lists after each expansion - as the expansions are exponential in nature and should be avoided
        short_set,long_set = ids_from_1,ids_from_2
        while degree > 0:
            if len(short_set) < len(long_set):
                temp_set = short_set
                short_set = long_set
                long_set = temp_set
            
            #test the first expansion
            self.expand_id_set(short_set)
            degree -= 1
            if self.check_matches(short_set,long_set):
                return True
 
            #test the second expansion if the number was even
            if degree > 0:
                self.expand_id_set(long_set)
                degree -= 1
                if self.check_matches(short_set,long_set):
                    return True
        return False
        
    #expand a set by adding the first-degree connections of each member in the set
    def expand_id_set(self,id_set):
        id_keys = list(id_set)
        for id_key in id_keys:        
            for linked in self.connections[id_key]:
                id_set.add(linked)

    #test for whether any item in the first set is also in the second set
    #it is better to loop through the shorter one
    def check_matches(self,id_set_1,id_set_2):
        short_set,long_set = (id_set_1,id_set_2) if len(id_set_1) < len(id_set_2) else (id_set_2,id_set_1)
            
        for _id in short_set:
            if _id in long_set:
                return True
        return False

#get ids from a line of input
#for this task you only need the id's
#for live use you would definitely want to check that all of the data is in the expected format
def get_ids_from_line(line):
    line_data = line.strip().split(",")

    #test that length is at least 4 (it should be 5, but the comment is irrelevant)
    if len(line_data) < 4:
        return None

    #confirm that the first field is a date of the form year-month-data hr:mn:sec
    
    #confirm that the second and third fields are integers and remove the white space
    line_data[1] = line_data[1].strip()
    if not line_data[1].isdigit():
        return None

    line_data[2] = line_data[2].strip()
    if not line_data[2].isdigit():
        return None

    #confirm that the 4th field is a number

    return line_data[1],line_data[2]

#updates the graph for a file of transcations
def process_batch (filname,connections):
    batch_fh = open(filname)
    heading = batch_fh.readline()
    for line in batch_fh:
        ids = get_ids_from_line(line)
        if ids is not None:
            connections.add_connection(ids[0],ids[1])

#determines whether a transaction is verified, and updates the graph
#writies "unverified" or "trusted" to the given output file
def process_streaming(input_filename, output_filename, connections, degree):
    input_fh = open(input_filename)
    output_fh = open(output_filename, 'w')

    heading = input_fh.readline()
    for line in input_fh:
        ids = get_ids_from_line(line)
        if ids is not None:

            #check whether the two id's are within the same degree-network
            if connections.in_network(ids[0],ids[1],degree):
                output_fh.write("trusted\n")
            else:
                output_fh.write("unverified\n")

            #add the connection
            connections.add_connection(ids[0],ids[1])
    
    output_fh.close()

def main (argv):
    #expects 2 files and 3 outputs depending on the task
    if len(argv) < 5:
        print("Not enough inputs: expected <batch_input> <streaming_input> <task_1_output> <task_2_output> <task_3_output>")
        return

    #get filenames
    batch_input = argv[0]
    streaming_input = argv[1]
    task_1_output = argv[2]
    task_2_output = argv[3]
    task_3_output = argv[4]

    #create graph object
    payment_graph = Payment_Graph()

    #batch process
    print("processing batch input...")
    process_batch(batch_input,payment_graph)
    print("finished processing batch input\n")

    #task 1
    task_graph = copy.deepcopy(payment_graph)
    print("processing streaming input for task 1...")
    process_streaming(streaming_input,task_1_output,task_graph,1)
    print("finished processing task 1\n")

    #task 2
    task_graph = copy.deepcopy(payment_graph)
    print("processing streaming input for task 2...")
    process_streaming(streaming_input,task_2_output,task_graph,2)
    print("finished processing task 2\n")

    #task 3
    task_graph = copy.deepcopy(payment_graph)
    print("processing streaming input for task 3...")
    process_streaming(streaming_input,task_3_output,task_graph,4)
    print("finished processing task 3\n")

if __name__ == "__main__":
    main(sys.argv[1:])



           

            
