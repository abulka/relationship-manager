# Program to experiment with the use of the super() 
# function in multiple levels of single inheritance 
# taked from https://www.geeksforgeeks.org/python-super-function-with-multilevel-inheritance/

class GFG1: 
	def __init__(self): 
		print('HEY !!!!!! GfG I am initialised(Class GEG1)') 

	def sub_GFG(self, b): 
		print('Printing from class GFG1:', b) 

# class GFG2 inherits the GFG1 
class GFG2(GFG1): 
	def __init__(self): 
		print('HEY !!!!!! GfG I am initialised(Class GEG2)') 
		super().__init__() 

    # CAN OMIT OR NOT - PROVES  the parent method need not have 
    # the method being invoked, it just has to be in the tree above it - as you would expect
    #
	# def sub_GFG(self, b): 
	# 	print('Printing from class GFG2:', b) 
	# 	super().sub_GFG(b + 1) 

# class GFG3 inherits the GFG1 ang GFG2 both 
class GFG3(GFG2): 
	def __init__(self): 
		print('HEY !!!!!! GfG I am initialised(Class GEG3)') 
		super().__init__() 
		# super()  # <--- this alone doesn't work and calls nothing !

	def sub_GFG(self, b): 
		print('Printing from class GFG3:', b) 
		super().sub_GFG(b + 1000)  # <- hoping this call reaches the top CFG1 class passing through the GFG2 class


# main function 
if __name__ == '__main__': 

	# created the object gfg 
	gfg = GFG3() 

	# calling the function sub_GFG3() from class GHG3 
	# which inherits both GFG1 and GFG2 classes 
	gfg.sub_GFG(10) 

