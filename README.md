# CS179M_TeamKitty
This is TeamKitty's CS179M AI project from UCR. The project consist on building a software for Mr.Keogh, owner Long Beach Keogh unloading bay.
The software consists in helping Mr. Keogh's crane operator to move containers inside a one bay ship out of the ship, load into the ship
or balance the ship in the least time possible. The software must do one job per ship's manifest only.

The manifests consists of information for every single container above the ship. The bay can be picture as an 8 by 12 grid, consisting of 96 containers
in total. The bay can have from 0 to 96 containers aboard the ship. The ship may also have spots at the bottom that may not be accessible for containers. 
Here is a little example of how the bay may look like.

![s3](https://user-images.githubusercontent.com/86257457/227685956-f90a349f-be18-4466-8ef2-511876b2df73.jpg)

Knowing all this, we created an idea on how the UI may look. Considering that Mr.Keogh is only asking for somethin simple that his workers can easily use
we decided to design a simple UI as asked. In the following image, we provide an initial mock-up design on how we picture the UI can look.
![Initial_setup](https://user-images.githubusercontent.com/86257457/227684348-9fea0224-c0db-4000-bf07-50a04a7c16a3.jpg)

The front-end is simple, but the the important part is that the program does provide an optimal number of movements inside the ship. Keeping that in mind, 
the design for the UI was kept as simple as possible. To do so, we used python's Tkinter tool, to create a program that would work on desktops or laptops. 
A little preview on how the program looks using Tkinter. 
![long_beach](https://user-images.githubusercontent.com/86257457/227687991-dd8fd0a1-06e8-429b-a046-9487fd4d5cae.png)

By using the manifests from the ships, we can upload the text file to our program in this will fill up the grid as how it will look like inside the ship.
![manifest](https://user-images.githubusercontent.com/86257457/227688397-5630be73-678b-42f1-9560-34a21c09fdbd.png)

Once the manifest is load to the program, we can select the type of job we want to do from the simple drop-menu. After the job is selected, the program 
will proceed to find the optimal movement. 
![jobs](https://user-images.githubusercontent.com/86257457/227688903-ae69978c-5fd9-4ad9-b752-70afaac50e42.png)

The program is fast in finding the solution. Once it does, we just proceed in clicking in the enabled "Next Move" button, which will then show the next container to 
move. This will continue until all containers selected have been moved. 



