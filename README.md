# kisan-expo
🌾 Kisan Expo — Empowering Agriculture Digitally      


python manage.py migrate                                                                                                                                                                      
python manage.py populate_app_models                                                                                                                                                          
python manage.py createsuperuser


| **Permission Name** | **Code** | **Description**          |
| ------------------- | -------- | ------------------------ |
| 🟢 Create           | `c`      | Allows creating entries  |
| 🔵 Read             | `r`      | Allows viewing data      |
| 🟡 Update           | `u`      | Allows modifying records |
| 🔴 Delete           | `d`      | Allows removing records  |

📦 Features

✅ Dynamic Role-Based Access System                                                                                                                                                       
✅ CRUD Permissions per Model (Create, Read, Update, Delete)                                                                                                                           
✅ Custom Permission Assignment via Modal UI                                                                                                                                        
✅ Local Time Logging of User Activities                                                                                                                                                
✅ Admin Interface & Superuser Management                                                                                                                                               
✅ Scalable App Model System        

📁 Project Structure                

accounts/ – Handles user authentication and profiles.

kisanexpo/ – Core application logic and settings.

templates/ – HTML templates for rendering views.

manage.py – Django's command-line utility.

requirements.txt – Python dependencies.


🛠️ Technologies Used

Backend: Django (Python)

Frontend: HTML, CSS

Database: SQLite (default)
