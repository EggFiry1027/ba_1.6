# Ballistica Linux 1.6 Server build
A TESTING Linux Ubuntu v20 server build for BombSquad/Ballistica 1.6
***
# SERVER SETUP INSTRUCTIONS
Follow the below steps after creating an EC2 Linux v20 AWS instance:
***
    #(1) After Creating an Ec2 instance in AWS, it should be Online, now execute the following command in SSH terminal:
        - sudo apt update && sudo apt dist-upgrade && sudo apt install python3-pip libopenal-dev libsdl2-dev libvorbis-dev cmake clang-format git
 
    #(2) Now clone the 1.6 server build from github using, 
        - git clone https://github.com/FireFighter1027/ba_1.6.git
    #(or) with ssh:
        - git clone git@github.com:FireFighter1027/ba_1.6.git
 
    #(3) Now we are ready to go, But we have to configure the settings and add admins/owners, Edit the following, 
        # - Edit config.yaml  - server name , size , port , admin .
        # - Open administrator_setup.py (ba_1.6/dist/ba_root/mods/administrator_setup.py)
        # first add your pb-ID/account_id in 'owners' variable as shown below:
        owners = ['pb-IF40V1hYXQ==']
        # and edit put the same name of your server, others things in there may not be needed, if you want, then read all things carefully and edit it.
        # - Edit roles.py to add admins,etc (ba_1.6/dist/ba_root/mods/roles.py)
        # - Edit TeamNames, Teamscolors in _multiteamsession.py (/dist/ba_data/python/ba/_multiteamsession.py).
 
    #(4) Now get back to ssh terminal and execute the following cmds to start the server:
        - cd ba_1.6/my_server
        - chmod 777 bombsquad_server
        - cd dist
        - chmod 777 bombsquad_headless
        - cd ..
        - tmux new -s 43210 #(we used 43210 as name of that tmux, so we can connect back again using that name)
        - ./bombsquad_server
 
     #(5) Now Server should run :P
***
# Feedback and Support
Contact me through Discord for all feedbacks, complaints/errors, suggestions, etc,
my discord id = `Eggu#6389` , `FireFighter1027#3441`
***
# Enjoy !
Happy Modding/Playing !
