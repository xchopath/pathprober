# Cheatsheet

### Find Web Login
```
# python3 pathprober.py -T targets.txt -P paths.txt -w "<input" -w2 'type="password"' -o admins.txt
```

### Find /.git/config
```
# python3 pathprober.py -T targets.txt -p /.git/config -w "[core]" -w2 "filemode =" -o gitconfigs.txt
```

### Find AWS Key
```
# python3 pathprober.py -T targets.txt -p / -w "AKIA" -o awskeys.txt
```
