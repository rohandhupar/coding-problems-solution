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