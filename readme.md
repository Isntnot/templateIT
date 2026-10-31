So the basics, i want to use my obsidians templates in nvim so i can create some notes without the 3 minute boot time of obsidian. 
# Pipeline
Name of file -> Get directory -> check for a tps file -> it cat to the file

## TPS File 
tps will be the file that will route everything deciding what template to use etc...

## Processing file
After TPS found the file, the next thing it is to process it. (i will get a example from my obsidian folder)
```md
---
links:
  - '[[<% tp.date.now("DD-MM-YYYY") %>]]'
tags:
  - Sanitizable
---
```
this actually makes my job a little easier. since every template function will start with template anyway..., so i can use that <% %> to get the command, check what is for.
