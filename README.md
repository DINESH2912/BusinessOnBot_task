The Social media website called Linkup was created with the multile functionality.

**The Tech Stacks used are**

1.HTML

2.CSS

3.Flask

4.Sqlite(3)

5.bcrypt

6.Flask-limiter


The Complete website is hosted in Microsoft azure -- https://linkkup.azurewebsites.net/register

Front end :

1.Login Page -- https://drive.google.com/file/d/1EjqpygI2ETag3h59YJTWNeW50QKglLuY/view?usp=sharing

2.Home Page -- https://drive.google.com/file/d/1Ae20QUTroGza42rskQSeAA8zVSMA_m6z/view?usp=sharing

3.Getting all users -- https://drive.google.com/file/d/1gCrkrG8vnTR1mlonF4cEL_wH97hCR9l4/view?usp=sharing

4.Writing Comments on other posts -- https://drive.google.com/file/d/1geEYjwk35uIsGhNq48A2ghm5UfHacAcz/view?usp=sharing



Backend-Task
1.Getting all users -- https://drive.google.com/file/d/1GBxNn0D2H5hYTyCTOqwiOSBR-hq1rDNa/view?usp=sharing

2.Getting the user details from username -- https://drive.google.com/file/d/1jQhaaFmVfl3NaoGBtKnP4CDzde-2dnpk/view?usp=sharing

3.Getting all post details -- https://drive.google.com/file/d/1UXmQz0CFJZDJwiSZHMeY2_Gz32YjNqgx/view?usp=sharing

4.Getting the post by the particular person -- https://drive.google.com/file/d/1AvrKzKKxNbmGtQsUAYb_LrCFvkhQ2_Tk/view?usp=sharing


Used the Sqlite Database server


**Users Attributes**

id: Unique identifier for the user.

username: Unique username for the user.

password: Password for the user's account.

admin: Indicator of whether the user is an admin.

dob: Date of birth of the user.

profile_photo: Binary data of the user's profile photo.



**Posts Attributes**

post_id: Unique identifier for the post.

user_id: Identifier of the user who posted the post.

date: Date and time when the post was created.

description: Text description of the post.

image_data: Binary data of the image attached to the post.

image_ext: File extension of the attached image.


The user id is act as the foreign key.





