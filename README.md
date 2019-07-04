# AgricultureFund

If you have some data that could manifest the specific filed's development, which means that the data contain several years' keypoints of the specific field and how those keypoints link to the next year's keypoints.


## Matters need attentions

1. The data set needs to satisfy ：（ex：‘2008.txt’）
    - the filename just like '2008.txt'
    - the formation of every single data needs to correspond to '2008.txt'
    - utf-8 encoding
  
2. run 'sankey.py'

3. copy 'links.txt' & 'nodes.txt' to ‘sankeyModel.html’

4. open 'sankeyModel.html' in browser
    - every column' ndoes have been clustered by subject term, which is consistent with a single line of data set.
    - each column represents each year's data, that is a singe txt file.
    - each node represents one theme, besides, one term contains several theme.
    - each link represents that the previous year's theme how to flow to the next year.
    - the width of link is the weight of theme in your data set
    
    
![sankey0307.png-231.4kB][1]


## Updates

1. Now users can change node's name by double clicking node, then follow the prompt, input the node's new name and confirm.

2. Users can also merge two nodes into one. just hold 'ctrl' button while dragging first node to second node.


  [1]: http://static.zybuluo.com/HelloDatoo/32rbnfk7dmov33fc4bw5e056/sankey0307.png
