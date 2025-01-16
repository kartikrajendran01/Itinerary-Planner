class Node:
    def __init__(self,val,next=None):
        self.val = val
        self.next = next

def best_route(distance_matrix,no_of_places):
	minimum_distance_cost=float('inf')
	head=route(distance_matrix,no_of_places,0)
	temp=head
	distance_cost=0
	while(head!=None):
		if(head.next!=None):
			distance_cost+=distance_matrix[head.val][head.next.val]
		head=head.next
	if(distance_cost<minimum_distance_cost):
		minimum_distance_cost=distance_cost
		best_route_head=temp
	if(no_of_places>1):
		head=route(distance_matrix,no_of_places,-1)
		temp=head
		distance_cost=0
		while(head!=None):
			if(head.next!=None):
				distance_cost+=distance_matrix[head.val][head.next.val]
			head=head.next
		if(distance_cost<minimum_distance_cost):
			minimum_distance_cost=distance_cost
			best_route_head=temp
		head=route_2(distance_matrix,no_of_places,0)
		temp=head
		distance_cost=0
		while(head!=None):
			if(head.next!=None):
				distance_cost+=distance_matrix[head.val][head.next.val]
			head=head.next
		if(distance_cost<minimum_distance_cost):
			minimum_distance_cost=distance_cost
			best_route_head=temp
		head=route_2(distance_matrix,no_of_places,1)
		temp=head
		distance_cost=0
		while(head!=None):
			if(head.next!=None):
				distance_cost+=distance_matrix[head.val][head.next.val]
			head=head.next
		if(distance_cost<minimum_distance_cost):
			minimum_distance_cost=distance_cost
			best_route_head=temp
		head=route_1(distance_matrix,no_of_places,0)
		temp=head
		distance_cost=0
		while(head!=None):
			if(head.next!=None):
				distance_cost+=distance_matrix[head.val][head.next.val]
			head=head.next
		if(distance_cost<minimum_distance_cost):
			minimum_distance_cost=distance_cost
			best_route_head=temp
		head=route_1(distance_matrix,no_of_places,1)
		temp=head
		distance_cost=0
		while(head!=None):
			if(head.next!=None):
				distance_cost+=distance_matrix[head.val][head.next.val]
			head=head.next
		if(distance_cost<minimum_distance_cost):
			minimum_distance_cost=distance_cost
			best_route_head=temp
	return best_route_head

def route(distance_matrix,no_of_places,alorithm_no):
    visited_status=[]
    maximum_distance = -1
    for i in range(no_of_places):
        visited_status.append(0)
        if(sum(distance_matrix[i])>maximum_distance):
            starting_index = i
            maximum_distance=sum(distance_matrix[i])
    visited_status[starting_index]=1
    head = Node(starting_index)
    best_route=next_place(distance_matrix,visited_status,head,no_of_places,head,alorithm_no)
    return best_route

def next_place(distance_matrix,visited_status,head,no_of_places,tail,alorithm_no):
	#head is the starting place of route and tail is the last place
    maximum_distance=0
    next_place_index=100000
    for i in range(no_of_places):
		#selects the distant place from the selected places
        distance_sum=0
        if(visited_status[i]==0):
            for j in range(no_of_places):
                if(visited_status[j]>alorithm_no):
                    distance_sum+=distance_matrix[j][i]
            if(distance_sum>maximum_distance):
                maximum_distance=distance_sum
                next_place_index = i
    
    if(next_place_index==100000):
        return head
    else:
		#places the place on the suitable position 
        distance = distance_matrix[tail.val][next_place_index]
        suitable_replacement=None
        temp=head
        while(temp.next!=None):
            new_distance = distance_matrix[temp.val][next_place_index]+distance_matrix[next_place_index][temp.next.val]-distance_matrix[temp.val][temp.next.val]
            if(new_distance<distance):
                distance = new_distance
                suitable_replacement = temp
            temp=temp.next
        visited_status[next_place_index]=1
        if(suitable_replacement!=None):
            temp=suitable_replacement.next
            suitable_replacement.next=Node(next_place_index)
            suitable_replacement.next.next=temp
        else:
            tail.next=Node(next_place_index)
            tail=tail.next
        return next_place(distance_matrix,visited_status,head,no_of_places,tail,alorithm_no)

def route_1(distance_matrix,no_of_places,algorithm_no):
    visited_status=[]
    maximum_distance = 0
    for i in range(no_of_places):
        visited_status.append(0)
        if(sum(distance_matrix[i])>maximum_distance):
            starting_index = i
            maximum_distance=sum(distance_matrix[i])
    visited_status[starting_index]=1
    head = Node(starting_index)
    path=next_place_1(distance_matrix,visited_status,head,no_of_places,head,algorithm_no)
    return path

def next_place_1(distance_matrix,visited_status,head,no_of_places,tail,algorithm_no):
    if(algorithm_no==0):
        maximum_distance=0
    else:
        minimum_disatnce=100000
    next_place_index=100000
    for i in range(no_of_places):
        if(algorithm_no!=0):
            if((visited_status[i]==0)&(distance_matrix[tail.val][i]+distance_matrix[i][head.val]<minimum_disatnce)):
                minimum_disatnce = distance_matrix[tail.val][i]+distance_matrix[i][head.val]
                next_place_index = i
                # print(minimum_disatnce)
        else:
            no_of_non_vsited_places=0
            for j in range(no_of_places):
                if(visited_status[j]==0):
                    no_of_non_vsited_places+=1
            no_of_visited_places=no_of_places-no_of_non_vsited_places
            distance_from_non_visited_places=0
            distance_from_visited_places=0
            if(visited_status[i]==0):
                for j in range(no_of_places):
                    if(visited_status[j]==1):
                        distance_from_visited_places+=distance_matrix[j][i]
                    else:
                        distance_from_non_visited_places+=distance_matrix[j][i]
                di=(distance_from_visited_places/no_of_visited_places)-(distance_from_non_visited_places/no_of_non_vsited_places)
                if(di>maximum_distance):
                    maximum_distance=di
                    next_place_index = i
    
    if(next_place_index==100000):
        return head
    else:
        # print(place_names[next_place_index])
        distance = distance_matrix[tail.val][next_place_index]
        suitable_replacement=None
        temp=head
        while(temp.next!=None):
            new_distance = distance_matrix[temp.val][next_place_index]+distance_matrix[next_place_index][temp.next.val]-distance_matrix[temp.val][temp.next.val]
            if(new_distance<distance):
                distance = new_distance
                suitable_replacement = temp
            temp=temp.next
        visited_status[next_place_index]=1
        if(suitable_replacement!=None):
            temp=suitable_replacement.next
            suitable_replacement.next=Node(next_place_index)
            suitable_replacement.next.next=temp
        else:
            tail.next=Node(next_place_index)
            tail=tail.next
        return next_place_1(distance_matrix,visited_status,head,no_of_places,tail,algorithm_no)

def route_2(distance_matrix,no_of_places,alorithm_no):
    visited_status=[0]
    maximum_distance = 0
    for i in range(no_of_places-1):
        visited_status.append(0)
        for j in range(i+1,no_of_places):
            if(distance_matrix[i][j]>maximum_distance):
                maximum_distance = distance_matrix[i][j]
                starting_index = i
                ending_index = j
    if(sum(distance_matrix[starting_index])<sum(distance_matrix[ending_index])):
        temp = starting_index
        starting_index = ending_index
        ending_index = temp
    visited_status[starting_index]=1
    visited_status[ending_index]=1
    head = Node(starting_index)
    head.next=Node(ending_index)
    return next_place_2(distance_matrix,visited_status,head,no_of_places,head.next,alorithm_no)

def next_place_2(distance_matrix,visited_status,head,no_of_places,tail,alorithm_no):
	#head is the starting place of route and tail is the last place
    maximum_distance=0
    next_place_index=100000
    for i in range(no_of_places):
		#selects the distant place from the selected places
        distance_sum=0
        if(visited_status[i]==0):
            distance_sum=distance_matrix[i][head.val]+distance_matrix[i][tail.val]
            if(distance_sum>maximum_distance):
                maximum_distance=distance_sum
                next_place_index = i
    
    if(next_place_index==100000):
        return head
    else:
		#places the place on the suitable position 
        distance = distance_matrix[tail.val][next_place_index]
        suitable_replacement=None
        temp=head
        while(temp.next!=None):
            new_distance = distance_matrix[temp.val][next_place_index]+distance_matrix[next_place_index][temp.next.val]-distance_matrix[temp.val][temp.next.val]
            if(new_distance<distance):
                distance = new_distance
                suitable_replacement = temp
            temp=temp.next
        visited_status[next_place_index]=1
        if((distance_matrix[next_place_index][head.val]<distance)&(alorithm_no==1)):
            temp=head
            head=Node(next_place_index)
            head.next=temp
        else:
            if(suitable_replacement!=None):
                temp=suitable_replacement.next
                suitable_replacement.next=Node(next_place_index)
                suitable_replacement.next.next=temp
            else:
                tail.next=Node(next_place_index)
                tail=tail.next
        return next_place_2(distance_matrix,visited_status,head,no_of_places,tail,alorithm_no)