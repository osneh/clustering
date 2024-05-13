# c_xypicmic



## Getting started

To make it easy for you to get started with GitLab, here's a list of recommended next steps.

Already a pro? Just edit this README.md and make it your own. Want to make it easy? [Use the template at the bottom](#editing-this-readme)!

## Add your files

- [ ] [Create](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#create-a-file) or [upload](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#upload-a-file) files
- [ ] [Add files using the command line](https://docs.gitlab.com/ee/gitlab-basics/add-file.html#add-a-file-using-the-command-line) or push an existing Git repository with the following command:

```
cd existing_repo
git remote add origin https://gitlab.in2p3.fr/h.abreu/c_xypicmic.git
git branch -M main
git push -uf origin main
```

## To compile
git clone https://gitlab.in2p3.fr/h.abreu/c_xypicmic.git

cd c_xypicmic

gcc -lm xypicmic.c xypicmic.c -o xypicmic.exe

-lm flag just make the link to the math's library ``link math``

## To run
./xypicmic.exe 50 6 103 35 34 37 75 10 88 44 6 15 68 28

## OR 
if you need to decode an ascii file produced by PICMIC-SAMPIC, you should first decode the ascci file to feed the xypicmic:
```
python ascii_readDataPicmic_bin2ascii.py -f your-ascii-file-produced-by-SAMPIC.txt > tmp.csv 
```
then to read and process the event by the c_xypimic; just run the follozing comand:
```
python xLinesPicmicOffile.py
``` 
