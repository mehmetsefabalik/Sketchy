
## CMPE 484 PROJECT
#### Mehmet Sefa BALIK 
#### Nesat DERELI

### PRESENTATION

- https://docs.google.com/presentation/d/101WA6ShiFHuLSU_ZpkgzbnxCMRDkSe9OrAbtOw5s_fc/edit?usp=sharing

### HOW TO RUN

```
git clone https://github.com/mehmetsefa2644/Sketchy.git

cd Sketchy

```

```
usage: sketchy_lines.py [-h] [-t1 THRESHOLD1] [-t2 THRESHOLD2] [-lw LINEWIDTH]
                        [-o OPACITY] [-ln VIDEOLENGTH]
                        input output

positional arguments:
  input            input image name
  output           output video name

optional arguments:
  -h, --help       show this help message and exit
  -t1 THRESHOLD1   Threshold for the dots, the bigger the threshold, the less
                   dots displayed
  -t2 THRESHOLD2   Threshold for the connected dots, the bigger the threshold,
                   the less connected dots displayed
  -lw LINEWIDTH    Width for the displayed lines
  -o OPACITY       Opacity for the dots
  -ln VIDEOLENGTH  Length of the video, the bigger this value, the longer
                   video


```

## DELIVERABLES

### Week 1:
- Edge detection of the given image (@nesat)
- Spliting image into grids (@mehmetsefa2644)


### Week 2:
- Detecting the grids which has points(non-zero sum)(@nesat)
- Combining related grids into a meaningful order(@mehmetsefa2644)


### Week 3:
- Building frames out of related grids(@nesat)
- Appending these frames to construct a video(@mehmetsefa2644)
