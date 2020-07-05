from collections import defaultdict
class Solution:
    def sortArrayByParity(self, A: List[int]) -> List[int]:
        new_list=defaultdict(list)
        a=['e' if i%2==0 else 'o' for i in A]
        for i , j in zip(a,A):
            new_list[i].append(j)
        
        b=new_list['o']
        c=new_list['e']
        
        for i in b:
            c.append(i)
        return c

class Solution:
    def smallerNumbersThanCurrent(self, nums: List[int]) -> List[int]:
        dic={}
        a=sorted(nums)
        for i , j in enumerate(a):
            if j not in dic:
                dic[j]=i
        return [ dic[n] for n in nums]

class Solution:
    def findUnsortedSubarray(self, nums: List[int]) -> int:
        start=len(nums)
        end=0
        if nums==sorted(nums):
            return 0
        else:
            for i in range(0,len(nums)-1):
                for j in range(i+1,len(nums)):
                    if nums[i]>nums[j]:
                        start=min(start,i)
                        end=max(end,j)
            return((end-start+1))
a = list(map(int, input().rstrip().split()))
leaders=[]
for i in range(len(a)-1):
    first=a[i]
    max_ele=max(a[i+1:])
    if first > max_ele:
        leaders.append(a[i])
leaders.append(a[-1])

class Solution:
    def search(self, nums: List[int], target: int) -> int:
        if len(nums)==0:
            return -1
        for i in range(len(nums)):
            if target in nums:
                return nums.index(target)
            else : 
                return -1
class Solution:
    def sortColors(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        arr=nums
        low=0
        high=len(arr)-1
        mid=0
        while(mid<=high):
            if(arr[mid]==0):
                arr[mid],arr[low]=arr[low],arr[mid]
                low+=1
                mid+=1
            elif(arr[mid]==1):
                mid+=1
            else:
                arr[mid],arr[high]=arr[high],arr[mid]
                high-=1
        nums=arr
        return nums
class Solution:
    def isIdealPermutation(self, A: List[int]) -> bool:
        
        ### every local inversion is global inversion 
        ### using a concept where you can find minmum and take whole left 
        ### values from minimum won't work because if case comes like 0,2,1
        ### then concept will fail 
        
        ### every local inversion is gobal inversion but vice and versa is not true
        
        for i ,j in enumerate(A):
            if abs(i-j)>1:
                return False
        return True
class Solution:
    def increasingTriplet(self, nums: List[int]) -> bool:
        count=0
        for i in range(1,len(nums)-1):
            if nums[i]>min(nums[:i]) and nums[i]<max(nums[i+1:]):
                count+=1
                
        if count>=1:
            return True
        else :
            return False
def removeX(string):
    if len(string)==0:
        return string 
    smallstring=removeX(string[1:])
    
    if string[0]=="x":
        return smallstring    
    else :
        return string[0]+smallstring 

# Main
string = input()
print(removeX(string))
def mergeSort(arr):
    if len(arr)>1:
        mid_value=len(arr)//2
        left=arr[:mid_value]
        right=arr[mid_value:]
        left=mergeSort(left)
        right=mergeSort(right)
        
        arr=[]
        
        while len(left)>0 and len(right)>0:
            if left[0]<right[0]:
                arr.append(left[0])
                left.pop(0)
            else:
                arr.append(right[0])
                right.pop(0)
                
        for i in left:
            arr.append(i)
        for i in right:
            arr.append(i)
    return arr 

# Main
n=int(input())
arr=list(int(i) for i in input().strip().split(' '))
arr=mergeSort(arr)
print(*arr)

def partition(arr,low,high): 
    i = ( low-1 )         # index of smaller element 
    pivot = arr[high]     # pivot 
  
    for j in range(low , high): 
  
        # If current element is smaller than the pivot 
        if   arr[j] < pivot: 
          
            # increment index of smaller element 
            i = i+1 
            arr[i],arr[j] = arr[j],arr[i] 
  
    arr[i+1],arr[high] = arr[high],arr[i+1] 
    return ( i+1 ) 
  
# The main function that implements QuickSort 
# arr[] --> Array to be sorted, 
# low  --> Starting index, 
# high  --> Ending index 
  
# Function to do Quick sort 
def quickSort(arr,low,high): 
    if low < high: 
  
        # pi is partitioning index, arr[p] is now 
        # at right place 
        pi = partition(arr,low,high) 
  
        # Separately sort elements before 
        # partition and after partition 
        quickSort(arr, low, pi-1) 
        quickSort(arr, pi+1, high) 
        
        
        
        

n=int(input())
arr=list(int(i) for i in input().strip().split(' '))
quickSort(arr, 0,len(arr)-1)
print(*arr)

