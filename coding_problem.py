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

