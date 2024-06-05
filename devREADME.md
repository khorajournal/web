# Khora Journal Dev Docs

### Overview

This Journal is inspired after Umbr(a), led by Joan Copjec. 

The Web Infrastructure of this Journal is being designed to be automated. A single config file will be in charge of dispensing the parameters required to generate the entire website. A snapshot system will be used wherein the current site configuration is stored. When there are changes in the generative config relative to the snapshot config, specific webpages altered by the config changes will see revision. This is done in order that the webisite is not regenerated as a whole. In analytical terms, such an operation may be imagined on average to run fairly quickly, but small changes like font on a specific journal entry gallery should not lead to some 10 pages or 100 pages or 1000 pages being regenerated. The runtime as such would be an orthogonal group of the number of webpages that comprise the entire website without the snapshot config convention. The hope is that a well designed snapshot system will allow for a runtime of a constant orthogonal group. Note that this is not parameterized by the size of the website. 

All media and pages that are not the default index will be found in the directory 'include'. 'updateweb.py' will handle checking the config file and snapshot and then generating new html upon demand.
