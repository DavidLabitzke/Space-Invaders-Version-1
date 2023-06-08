# Space invaders Version 1

This is my first attempt at making a game on my own in pygame. I decided to go with a space invaders game. While I am overall satisfied with the project, there are a number of issues that I feel should be addressed. 

## Issues to address
1. Sound. I would like to create a sound manager file, to handle sound effects and background sounds. 
2. Code readability. At first, I thought that including multiple files for the classes would improve readability. However, upon further inspection, I see that it has actually made the code less readable, as well as give way to potential performance issues. 
3. Using sprite groups. After I was nearing completion of this project, I learned there was a feature in pygame classed sprite groups. This essentially allows you to manage multiple objects on screen at once. This would have made programming this game a lot easier had I known about this sooner. 
4. Glitch with enemy shooting. Enemies are only meant to fire when there are no other enemies beneath them. Unfortunately, this issue is still persisting, even after I implemented code to catch this glitch. 
5. Separate spaceship enemy class. Simply put, the spaceship enemy should have its own class. While it shares a lot of similarities with the other on screen enemies, its behavior is different enough that it lead to me making a lot of changes to the enemy class that are targetted specifically for this class. 
