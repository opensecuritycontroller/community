# [Defect Title]

**Defect number:** DE2801  
**Defect Title:** Job Graph is not displayed well if special characters - “{“ and “}” are used in the Manager Connector (MC) Name  
**Severity:** Cosmetic

**Initial state:**  
Have an OSC deployed

**Steps:**  
1. Create any manager connector with the next name NORMAL BLACK " NODE }      

**Actual Result:**  
The job graphs for the creation or edit of the manager connector will be: NORMAL => will look normal BLACK " => Will look like one line with some black rectangles NODE } => will look like graph but will have the node names modified same for NODE {.

**Expected Result:**  
All the job graphs are supposed to look normal (no black rectangles).  

**Work around:**  
Do not use the special characters “{“ and “}” in the Manager Connector Name.

****

