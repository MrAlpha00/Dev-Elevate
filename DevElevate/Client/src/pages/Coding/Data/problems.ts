import type { Problem } from '../Types';

export const problems: Problem[] = [
  {
    id: '1',
    title: 'Two Sum',
    description: `Given an array of integers \`nums\` and an integer \`target\`, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.`,
    difficulty: 'Easy',
    category: 'Array',
    tags: ['Array', 'Hash Table'],
    examples: [
      {
        input: 'nums = [2,7,11,15], target = 9',
        output: '[0,1]',
        explanation: 'Because nums[0] + nums[1] == 9, we return [0, 1].'
      },
      {
        input: 'nums = [3,2,4], target = 6',
        output: '[1,2]'
      }
    ],
    constraints: [
      '2 ≤ nums.length ≤ 10⁴',
      '-10⁹ ≤ nums[i] ≤ 10⁹',
      '-10⁹ ≤ target ≤ 10⁹',
      'Only one valid answer exists.'
    ],
    testCases: [
      {
        id: '1',
        input: '[2,7,11,15]\n9',
        expectedOutput: '[0,1]',
        hidden: false
      },
      {
        id: '2',
        input: '[3,2,4]\n6',
        expectedOutput: '[1,2]',
        hidden: false
      },
      {
        id: '3',
        input: '[3,3]\n6',
        expectedOutput: '[0,1]',
        hidden: true
      }
    ],
    acceptance: 47.8,
    submissions: 4250000,
    starterCode: {
      'python': `def twoSum(nums, target):
    """
    :type nums: List[int]
    :type target: int
    :rtype: List[int]
    """
    pass`,
      'javascript': `/**
 * @param {number[]} nums
 * @param {number} target
 * @return {number[]}
 */
var twoSum = function(nums, target) {
    
};`,
      'java': `class Solution {
    public int[] twoSum(int[] nums, int target) {
        
    }
}`,
      'cpp': `class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        
    }
};`,
      'c': `/**
 * Note: The returned array must be malloced, assume caller calls free().
 */
int* twoSum(int* nums, int numsSize, int target, int* returnSize){
    
}`
    },
    createdAt: '2024-01-15T10:00:00Z'
  },
  {
    id: '2',
    title: 'Reverse Integer',
    description: `Given a signed 32-bit integer \`x\`, return \`x\` with its digits reversed. If reversing \`x\` causes the value to go outside the signed 32-bit integer range [-2³¹, 2³¹ - 1], then return 0.

**Assume the environment does not allow you to store 64-bit integers (signed or unsigned).**`,
    difficulty: 'Medium',
    category: 'Math',
    tags: ['Math'],
    examples: [
      {
        input: 'x = 123',
        output: '321'
      },
      {
        input: 'x = -123',
        output: '-321'
      },
      {
        input: 'x = 120',
        output: '21'
      }
    ],
    constraints: [
      '-2³¹ ≤ x ≤ 2³¹ - 1'
    ],
    testCases: [
      {
        id: '1',
        input: '123',
        expectedOutput: '321',
        hidden: false
      },
      {
        id: '2',
        input: '-123',
        expectedOutput: '-321',
        hidden: false
      },
      {
        id: '3',
        input: '120',
        expectedOutput: '21',
        hidden: true
      }
    ],
    acceptance: 25.7,
    submissions: 3100000,
    starterCode: {
      'python': `def reverse(x):
    """
    :type x: int
    :rtype: int
    """
    pass`,
      'javascript': `/**
 * @param {number} x
 * @return {number}
 */
var reverse = function(x) {
    
};`,
      'java': `class Solution {
    public int reverse(int x) {
        
    }
}`,
      'cpp': `class Solution {
public:
    int reverse(int x) {
        
    }
};`
    },
    createdAt: '2024-01-16T14:30:00Z'
  },
  {
    id: '3',
    title: 'Longest Common Subsequence',
    description: `Given two strings \`text1\` and \`text2\`, return the length of their longest common subsequence. If there is no common subsequence, return 0.

A subsequence of a string is a new string generated from the original string with some characters (can be none) deleted without changing the relative order of the remaining characters.

For example, "ace" is a subsequence of "abcde".

A common subsequence of two strings is a subsequence that is common to both strings.`,
    difficulty: 'Hard',
    category: 'Dynamic Programming',
    tags: ['String', 'Dynamic Programming'],
    examples: [
      {
        input: 'text1 = "abcde", text2 = "ace"',
        output: '3',
        explanation: 'The longest common subsequence is "ace" and its length is 3.'
      },
      {
        input: 'text1 = "abc", text2 = "abc"',
        output: '3',
        explanation: 'The longest common subsequence is "abc" and its length is 3.'
      }
    ],
    constraints: [
      '1 ≤ text1.length, text2.length ≤ 1000',
      'text1 and text2 consist of only lowercase English characters.'
    ],
    testCases: [
      {
        id: '1',
        input: '"abcde"\n"ace"',
        expectedOutput: '3',
        hidden: false
      },
      {
        id: '2',
        input: '"abc"\n"abc"',
        expectedOutput: '3',
        hidden: false
      },
      {
        id: '3',
        input: '"abc"\n"def"',
        expectedOutput: '0',
        hidden: true
      }
    ],
    acceptance: 58.9,
    submissions: 890000,
    starterCode: {
      'python': `def longestCommonSubsequence(text1, text2):
    """
    :type text1: str
    :type text2: str
    :rtype: int
    """
    pass`,
      'javascript': `/**
 * @param {string} text1
 * @param {string} text2
 * @return {number}
 */
var longestCommonSubsequence = function(text1, text2) {
    
};`,
      'java': `class Solution {
    public int longestCommonSubsequence(String text1, String text2) {
        
    }
}`,
      'cpp': `class Solution {
public:
    int longestCommonSubsequence(string text1, string text2) {
        
    }
};`
    },
    createdAt: '2024-01-17T09:15:00Z'
  }
];