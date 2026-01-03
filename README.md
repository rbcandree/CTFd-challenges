# CTFd-challenges

Challenges can be downloaded as‑is.

To build a challenge, open a Terminal, navigate to its directory, and run:
- docker build -t <image_name> .

After building, you can launch the challenge with:
- docker run -d --name container_name -p 9000:22 -p 9001:80 image_name

For additional information, see the description.pdf file.

-----

The Run challenge based on the Chromium Dino game.

It includes modified source code from:
- The Chromium Authors (BSD License)
- Dino game by 牛さん (BSD 3-Clause License)

All original licenses and copyright notices are preserved as required.
