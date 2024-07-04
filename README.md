# image-sorter

Coded by chatGPT

## Writing an image sorter with ChatGPT.

I have a Camera Roll folder that’s 125 GB. Many of the images are duplicates spread across different subfolders. I want a script that lists all the duplicate images in a CSV file. The start point was the following prompt to chatGPT  ```
Make a Python image sorter with the following actions: 1. Crawl through a given directory and all it's subfolders 2. Output all files with the same file name to a csv file. Include the full path and file name, date the photo was taken, and file size as columns in the file
```

Not wanting to edit the code every time I wanted to run the script I added 

```
modify the scrip so I can pass the path as an arguement
```

The code produced combed through the directories and pull all the data in a dictionary, and output the dictionary to the output folder. 

This wasn’t great because I would get no output until the dict was filled, and I didn’t know how long it would run. The next prompt was  ``` modify the code so it writes to output.csv every 50 images then clear the dict and start again ```

I had the output I could follow along with and saw I wanted to modify the output data.  Instead of one output file with all duplicates I want to split it up into sets of 50. 

```
Write the file size in MB. Include the full path of both files that are duplicated.
Only write the path relative to the first shared directory of both files.
```

```
Instead of one output file, increment the the output filename with 1 every 50 duplicated files found
```

```
If the file has no EXIF data, only keep the filename and igore all other data
```

After these changes the ChatGPT script broke. I combined all the prompts into one prompt and started a new script from scratch. 

```
Make a Python image sorter with the following actions: 1. Crawl through a given directory and all it's subfolders 2. Output all files with the same file name to a csv file. Include the path relative to the first shared directory of both files, the path of both duplicates, date the photo was taken, and file size in MB as columns in the file. 3. I can pass the root direcotry as a parameter to the script 4. the script writes to output.csv every 50 duplicates found and contineus again 5. If the image file has no EXIF data, only keep the filename and igore all other data
```

The produced script errored, I pasted the script into chatGPT and told it fix the script. 

The produced script runs, but does not batch the results in sets of 50.

´´´ batch the output into sets of 50 and increment the output.csv file by numbering the file name
```

The script now runs and behaves as I intended. Time spent 45 minutes. 
Code on Github

https://github.com/a-bangk/image-sorter

