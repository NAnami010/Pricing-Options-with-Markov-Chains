from itertools import product
import math
import time
#To generate the path like "010" 0-> Price going down 1-> Price going up
def path_generate(n): 
	path_list=list(product(range(2),repeat=n))
	path_sum=[]
	for i in path_list:	
		path=[]
		for k in i:
			k=str(k)
			path.append(k)
		path_code=",".join(path) 	
		path_sum.append(path_code)	
			
	return path_sum
#This function is used to calculate the price for path in str like "010"
def Price_t(path,price_0,u,d): 
	up=0
	down=0
	path_list=path.split(",")
	for i in path_list:
		if i=="1":
			up=up+1
		else:
			down=down+1
	price_t=price_0*(u**up)*(d**down)
 
	return price_t
#This function is used to calculate path in list like [1,0,1]
def Price_t_for_list(path,price_0,u,d): 
	up=0
	down=0
	for i in path:
		if i==1:
			up=up+1
		else:
			down=down+1
	
	price_t=price_0*(u**up)*(d**down)
	return price_t

# Return the max price along the path. e.g when path
# is "01110" the max price is price of the third 1 
def Price_max(path,price_0,u,d): 
	price_list=[]
	path_list=path.split(",")
	num_path_list=[]
	for a in path_list:
		a=int(a)
		num_path_list.append(a)
	for i in range(len(num_path_list)+1):
		sub_path=num_path_list[:i]
		price_t=Price_t_for_list(sub_path,price_0,u,d)
		price_list.append(price_t)

	
	price_max=max(price_list)
	return price_max
	
# Return the "state" in time t, state
# is a list contain price S in time t
# and the max price along the path
def State_t(path,price_0,u,d):
	state=[]
	price_t=Price_t(path,price_0,u,d)
	price_max=Price_max(path,price_0,u,d)
	state.append(price_t)
	state.append(price_max)
	state=tuple(state)

	return state
	
	
# For every time point t, this function
# returns two state (price going up or down)
# in time t+1
def State_next(path,price_0,u,d):
	state_next=[]
	state_now=State_t(path,price_0,u,d)
	next_state_up=[]
	next_state_down=[]
	
	next_state_up.append(u*state_now[0])
	next_state_up.append(max(state_now[1],u*state_now[0]))
	next_state_down.append(d*state_now[0])
	next_state_down.append(state_now[1])
	
	state_next.append(tuple(next_state_up))
	state_next.append(tuple(next_state_down))
	
	return state_next

# Return a dictionary at last, in which the key is
# path like "010" and the element is the state
def final_state_dic(path_sum,price_0,u,d):
	path_dic={}
	for i in path_sum:
		state_all=[]
		state_now=State_t(i,price_0,u,d)
		state_next=State_next(i,price_0,u,d)
		state_all.append(state_now)
		for a in state_next:
			state_all.append(a)
		path_dic[i]=state_all
		
	return path_dic

# Return a dictionary , in which the key is
# state  [Price_t, Max Price] and the element is the value of option
def state_value_dic(path_dic,p,q,r):
	state_value_dic={}
	for path in path_dic:
		state_now=path_dic[path][0]
		value=state_now[1]-state_now[0]
		state_now_str=str(state_now)
		state_value_dic[state_now]=value

	return state_value_dic

def pricing(r,n,u,d,p,q,price_0):
	path_sum=path_generate(n)
	path_state_dic=final_state_dic(path_sum,price_0,u,d)
	value_dic=state_value_dic(path_state_dic,p,q,r)
	print(value_dic)
	print(value_dic)
	for i in range(n-1,0,-1):
		sub_path_state_dic=final_state_dic(path_generate(i),price_0,u,d)

		for path in sub_path_state_dic:
			value=(value_dic[sub_path_state_dic[path][1]]*p+value_dic[sub_path_state_dic[path][2]]*q)/(1+r)
			state_now=sub_path_state_dic[path][0]
			value_dic[state_now]=value

	u_1=tuple(list[price_0*u,price_0*u])
	d_1=tuple(list([price_0*d,price_0]))
	
	return (value_dic[u_1]*p+value_dic[d_1]*q)/(1+r)

# An example to pricing a lookback option for t=5 to 16
# risk-free rate is 5% T=1/12 sigma=20%
for N in range(5,16):	
	deltat = 1/(12*N)
	r =  math.exp(0.05*deltat)-1
	u = math.exp(math.sqrt(deltat)*0.2)
	d = 1/u
	p =  (1+r-d)/(u-d)
	q = 1-p
	print(pricing(r,N,u,d,p,q,1))	
	ed=time.time()
	tm=ed-st
	print(tm)