import pygame
import os
import sys
import time
import datetime
import random
import ctypes
import math
import gui_checkbox
from mycrypt import *
from myHighscore import *
  

#----------Backend variables----------#

#Check whether the app is running as a .py or .exe
#Assign name of app file accordingly
if getattr( sys, 'frozen', False ) :
    # running in a bundle (.exe)
    main_file = sys.executable
else :
    # running live (.py)
    main_file = __file__


# path is the directory where this program is stored
path = os.path.dirname(main_file)


#----------Initialize Game window----------#
pygame.init()
fullscreen = False
WIDTH,HEIGHT = 800,500
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Hangman Game!")

#----------Colors----------#
L_GREY = (200,200,200)
WHITE = (255,255,255)
GREY = (100,100,100)
BLACK = (0,0,0)
RED = (255,30,30)
GREEN = (0,200,0)
D_GREEN = (10,130,60)
L_GREEN = (180,230,30)
OLIVE = (160,200,30)
BLUE = (30,30,255)
L_BLUE = (0,160,230)
ORANGE = (220,100,0)
GOLDEN = (230,170,0)
SILVER = (130,130,130)
D_ORANGE = (150,50,0)
PURPLE = (150,0,150)

#----------Fonts----------\

LETTER_FONT = pygame.font.SysFont('verdana',28)
WORD_FONT = pygame.font.SysFont('verdana',35)
PARA_FONT = pygame.font.SysFont('showcardgothic',40)
OPTION_FONT = pygame.font.SysFont('showcardgothic',25)
LEADER_FONT = pygame.font.SysFont('showcardgothic',30)
SCORE_FONT = pygame.font.SysFont('showcardgothic',30)
HUD_FONT = pygame.font.SysFont('showcardgothic',25)
INFO_FONT = pygame.font.SysFont('arial black',18)


#----------Initialize Variables----------#


scene = "OPTIONS"
prev_scene = "INTRO"
word = "DEVELOPER"
questions = [] #images
answers = [] #strings
running = True
game_states=["not picked any word", "word ready to be guessed","word guessed","word failed to be guessed"]
game_state=0
man_state = 0
random_index = 0
chkboxes = [ ]
options_starty = 120
options_gap = 40
leader_starty = 120
leader_gap = 40
checked_options = []
total_score = 0
letter_streak = 0
order_matters = False
score_change = 0
score_change_info = [0,0,0,''] #[time at which score changed, current time, guess was right or wrong?,compliment]
default_lives = 2
lives = default_lives
compliments = ('','Good!','Keep it up!','Very Good!','Superb!','Incredible!!','UNREAL!!!!!!!!!!')
critics = ("Wrong letter!","Not that either!","Try something else!","Careful!!!","Last chance!!!")
win_msg = "Word Complete!"
level = 1
level_point = (3,6,9,12) #Words that need to won before going to a level
level_info = ('','',
              ["Good! Let's make this a bit tougher","Now in level 2, the empty blanks will","be hidden until you make 2 mistakes."],
              ["Well played! But can you win level 3?","This time the empty blanks will be","hidden until you make 4 mistakes!"],
              ["Amazing! In level 4, you must enter","letters in correct order.","This will be tough!"],
              ["This is the final level!","The blanks will be hidden until","you make 2 mistakes."])
words_guessed = [0,0] #two values; words guessed correctly,total words played
leaderboard_limit = 5 #maximum number of records in the leaderboard
game_over = False #if not False then it states the reason for game over, such as 'questions over'
player_inserted = True #flag to check if player inserted in leaderboard records
player_registered = True

#----------Initialize Letter Buttons----------#
#8 Letters per row -> 7 gaps + 8 circles + 2*sidegaps
RADIUS = 18
GAP = 10
SIDEGAP = (WIDTH/2 - 7*GAP - 8*(RADIUS*2))/2 
letters = []
guesses = []
starty = 320
#A to X
for i in range(24):
    l_x = SIDEGAP + RADIUS + (i%8)*(RADIUS*2 + GAP)
    l_y = starty + (i//8)*(GAP + RADIUS*2)
    letters.append([l_x,l_y,chr(i+65),True])
#Y
l_x = SIDEGAP + RADIUS + 3*(RADIUS*2 + GAP)
l_y += GAP + RADIUS*2
letters.append([l_x,l_y,'Y',True])
#Z
l_x += RADIUS*2 + GAP
letters.append([l_x,l_y,'Z',True])


#----------------------------------------#
#----------------------------------------#
#***************FUNCTIONS***************#
#----------------------------------------#
#----------------------------------------#


#Display Error Window
def error(title,msg):
    ctypes.windll.user32.MessageBoxW(0,msg,title,0)
    pygame.quit()


def safe_error(title,msg):
    ctypes.windll.user32.MessageBoxW(0,msg,title,0)

def screenCover():
    s = pygame.Surface((WIDTH,HEIGHT))
    s.set_alpha(128)
    s.fill((255,255,255))
    screen.blit(s,(0,0))
    
    pygame.display.update()

def hovers(obj, o_x, o_y):
    m_x, m_y = pygame.mouse.get_pos()
    if o_x <= m_x <= (o_x + obj.get_width()) and o_y <= m_y <= (o_y + obj.get_height()):
        return True
    else:
        return False
        
#Load image from specified path with specified resolution
def loadImage(image_path,size=(None,None)): #image_path is location of image file withing Hangman/Data folder.
    img = pygame.image.load(os.path.join(path,"data/"+image_path))
    if size!=(None,None):
        img = pygame.transform.scale(img,size)
    else:
        pass
    return img


def loadQuestion(file_name,image,topic):
    answer = file_name[:-4]
    answers.append(answer.upper())
    questions.append(image)

#Draw circular letter buttons
def drawLetters():
    m_x,m_y = pygame.mouse.get_pos()
    for letter in letters:
        x,y,ltr,visible=letter
        ltr_distance = math.sqrt((x - m_x)**2+(y - m_y)**2)           
        if visible:
            if ltr_distance <= RADIUS:
                pygame.draw.circle(screen,(160,230,30),(x,y),RADIUS,0)
            else:
                pygame.draw.circle(screen,L_BLUE,(x,y),RADIUS,0)
            pygame.draw.circle(screen,WHITE,(x,y),RADIUS,2)
            text = LETTER_FONT.render(ltr,1,WHITE)
            screen.blit(text,(x - text.get_width()/2,y - text.get_height()/2))


#Draw given message centered on a white screen for 3 seconds.
def drawMessage(message,seconds = 1):
    screen.fill(WHITE)
    text = WORD_FONT.render(message,1,BLACK)
    screen.blit(text,(WIDTH/2 - text.get_width()/2,HEIGHT/2 - text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(int(seconds*1000))
         

def showInfo(title,message_list):
    global scene
    prev_scene = scene
    scene = "INFO"
    screen.fill(GREY)
    screen.blit(bg,(0,0))
    while scene == "INFO":
        #Draw board and text
        screen.blit(board2,(WIDTH/2 - board2.get_width()/2,HEIGHT/2 - board2.get_height()/2))
        text = PARA_FONT.render(title,1,ORANGE)
        screen.blit(text,(WIDTH/2 - text.get_width()/2,HEIGHT/2 - 100))
        for i,message in enumerate(message_list):
            text = INFO_FONT.render(message,1,D_ORANGE)
            screen.blit(text,(WIDTH/2 - text.get_width()/2,HEIGHT/2- 60 + 30*i))
        
        #Draw ok button
        m_x,m_y = pygame.mouse.get_pos()
        ok_btn_y = HEIGHT/2 + 30 #this is local variable
        if hovers( ok_btn, ok_btn_x, ok_btn_y):
            screen.blit(ok_btn_green,(ok_btn_x,ok_btn_y))
        else:
            screen.blit(ok_btn,(ok_btn_x,ok_btn_y)) 
        
        pygame.display.update()
        
        for event in pygame.event.get():
            #Pressed Enter
            if event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key)
                key = key.upper()
                if key == "RETURN":
                    scene = prev_scene
            #Mouse Click Event
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x,m_y = pygame.mouse.get_pos()
                #If clicks ok then go to previous scene
                if hovers( ok_btn, ok_btn_x, ok_btn_y):
                    scene = prev_scene
                    


    
def drawCross():
    m_x,m_y = pygame.mouse.get_pos()
    if hovers( cross, cross_x, cross_y):
        screen.blit(cross_red,(cross_x, cross_y))
    else:
        screen.blit(cross,(cross_x, cross_y))


def drawLB():
    m_x,m_y = pygame.mouse.get_pos()
    if hovers( lb, lb_x, lb_y):
        screen.blit(lb_green,(lb_x, lb_y))
    else:
        screen.blit(lb,(lb_x, lb_y))


def letterInput(ltr):
    global total_score
    global man_state
    global letter_streak
    global score_change
    global score_change_info
    
    guesses.append(ltr)
    #If order does not matter then check if the letter is in word
    #Else, check if word formed in guesses is in word
    if (not order_matters and ltr in word) or order_matters and ''.join(guesses) == word[:len(guesses)]:
        if letter_streak > 0:
            letter_streak += 1
        else:
            letter_streak = 1
        score_change = 10*(2**(letter_streak-1))
        total_score += score_change
        if total_score > 999999:
            total_score = 999999
        compliment = compliments[(letter_streak - 1) if letter_streak <= 6 else 6]
        
        won = True
        if order_matters:
            won = False
            for letter in letters:
                letter[3] = True
            if word == ''.join(guesses):
                won = True       
        else:
            for letter in word:
                if letter not in guesses:
                    won = False
                    break
        if won:
            compliment = win_msg
        score_change_info = [datetime.datetime.now(),0,'right',compliment]
        
    else:
        if letter_streak < 0:
            letter_streak -= 1
        else:
            letter_streak = -1
        man_state += 1
        score_change = -5*(2**(-letter_streak-1))
        total_score += score_change
        if total_score < 0:
            total_score = 0
        critic = critics[man_state - 1] if man_state < 6 else " :(  it was " + word
        score_change_info = [datetime.datetime.now(),0,'wrong',critic]
        if order_matters:
            guesses.pop()
        
def dummieKey():
    #take dummie key inputs for 0.1 seconds
    time_a = datetime.datetime.now()
    while (datetime.datetime.now() - time_a).total_seconds() < 0.1:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                dummie_key = pygame.key.name(event.key)
                dummie_key = dummie_key.upper()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                m_x,m_y = pygame.mouse.get_pos()


def game_over_reset():
    global word
    global game_state
    global man_state
    global checked_options
    global guesses
    global questions
    global answers
    global letter_streak
    global total_score
    global letters
    global lives
    global level
    global words_guessed
    word = 'DEVELOPER'
    game_state = 0
    man_state = 0
    checked_options = []
    guesses = []
    questions = []
    answers = []
    letter_streak = 0
    total_score = 0
    lives = default_lives
    level = 1
    words_guessed = [0,0]
    for letter in letters:
        letter[3] = True

#----------Scene INTRO----------#
def runIntro():
    drawMessage("Welcome to Hangman!",3)


#----------Scene OPTIONS----------#
def runOptions():
    global checked_options
    global scene

    #----------Draw Options Menu
    screen.fill(GREY)
    screen.blit(bg,(0,0))
    screen.blit(board1,(WIDTH/2 - board1.get_width()/2,20))
    text = PARA_FONT.render('CHOOSE TOPICS :-',1,ORANGE)
    screen.blit(text,(WIDTH/2 - text.get_width()/2,37))
    i = 0
    checked_options = []
    for chkbox in chkboxes:
        chkbox.render_checkbox()
        text = OPTION_FONT.render(options[i],1,D_ORANGE)
        screen.blit(text,(200,options_starty + 10 + i*options_gap))
        if chkbox.is_checked():
            checked_options.append(chkbox)
        i += 1
    #Start Button appears Blue if at least one option is checked.
    #If no options are checked, then start button appears Grey.
    if len(checked_options) > 0:
        m_x,m_y = pygame.mouse.get_pos()
        if hovers( start_btn, start_btn_x, start_btn_y):
            screen.blit(start_btn_green,(start_btn_x,start_btn_y))
        else:
            screen.blit(start_btn,(start_btn_x,start_btn_y)) 
    else:
        screen.blit(start_btn_grey,(start_btn_x,start_btn_y))

    #Draw icons
    drawCross()
    drawLB()
    
    clickedStart = False
    #----------Events
    for event in pygame.event.get():
        #On QUIT Event runQuit
        if event.type == pygame.QUIT:
            runQuit()

        #If presses Enter and at least one option checked, start game
        elif event.type == pygame.KEYDOWN and len(checked_options) > 0:
            key = pygame.key.name(event.key)
            key = key.upper()
            if key == "RETURN":
                clickedStart = True
        
        #Mouse Click Event
        elif event.type == pygame.MOUSEBUTTONDOWN:
            m_x,m_y = pygame.mouse.get_pos()
            #If clicks Cross then runQuit
            if hovers( cross, cross_x, cross_y):
                runQuit()

            #if clicks lb, view leaderboard
            elif hovers( lb, lb_x, lb_y):
                viewLeaderboard()
                dummieKey()
                
            #If clicks Start Button, load question images from selected topics and change scene to GAME
            elif hovers( start_btn, start_btn_x, start_btn_y) and len(checked_options) > 0:
                clickedStart = True
                
        
        #Update Event in checkbox
        for chkbox in chkboxes:
            chkbox.update_checkbox(event)

    if clickedStart:
        print('Loading images...')
        text = INFO_FONT.render('Loading images...',1,WHITE)
        screen.blit(text,(WIDTH/2 - text.get_width()/2,380))
        pygame.display.update()
        for topic in checked_options: #topic is of type Checkbox
            i = -1
            for chkbox in chkboxes:
                i+=1
                if chkbox == topic:
                    # i is used to find index of checked checkboxes to get its corresponding string value
                    topic_name = options[i]
                    path_topic = os.path.join(path,'data/'+ topic_name)
                    #Read all files and folders from path\option
                    for Element in os.listdir(path_topic):
                        #Only consider files, exclude folders
                        if os.path.isfile(os.path.join(path_topic,Element)):
                            #Encrypt unencrypted files
                            if Element[-4:] == '.jpg':
                                image = loadImage(topic_name + '/' + Element,(400,400))
                                loadQuestion(Element, image,topic_name)
                                newname = encrypt.filename(Element,'ufyaixto',8)
                                os.rename(os.path.join(path_topic,Element),os.path.join(path_topic,newname))
                            #Decrypt Element name
                            truename = decrypt.filename(Element,'ufyaixto',8)
                            if truename[-4:] == '.jpg':
                                image = loadImage(topic_name + '/' + Element,(400,400))
                                loadQuestion(truename, image,topic_name)
                            else:
                                continue
        print("Images loaded!")
        scene = "GAME"
        prev_scene = "OPTIONS"
        dummieKey()
    

#----------Scene GAME----------#
def runGame():
    global scene
    global game_state
    global man_state
    global random_index
    global word
    global answers
    global questions
    global guesses
    global letter_streak
    global order_matters
    global total_score
    global score_change
    global score_change_info
    global game_over
    
    #Pick a word if game_state is 0 (i.e not yet picked)
    #Ignore if-else block if game_state is 1 (if word picked)
    #If game_state is 2 (next word), then set it back to 0 and do same action of game_state = 0 and set it to 1
    #If game_state is 3 (out of guesses/lost), then set it back to 0 and set scene to 'OPTIONS' as game is lost
    if game_state == 0:
        try: 
            # We can only get an error if answers is an empty list
            # That implies no question images could be loaded
            random_index = random.randint(0,len(answers)-1)
        except:
            safe_error("Question Images Not Found!",'''Image files for questions could not be loaded.
Please check the data folder and ensure that at least one question image exists in the selected topics folder.''')
            # Reset variables and go to options scene
            game_state = 0
            man_state = 0
            checked_options = []
            guesses = []
            questions = []
            answers = []
            for letter in letters:
                letter[3] = True
            scene = "OPTIONS"
            return
        game_state = 1
    #Word guessed correctly
    elif game_state == 2:
        #Remove the chosen word from answers and questions so that it does not repeat
        answers.pop(random_index)
        questions.pop(random_index)
        game_state = 0
        #Below try-except checks if run out of questions. If yes then game is over and we return to options
        try:
            random_index = random.randint(0,len(answers)-1)
        except ValueError:
            game_over = 'questions over'
            showInfo('WORDS OVER',['No more words remaining.','You can add more words in the','topics folder'])
            return     
        guesses = []
        game_state = 1
        man_state = 0
        letter_streak = 0
        for letter in letters:
            letter[3] = True
        return
    #Word not guessed
    elif game_state == 3:
        game_state = 2
        man_state = 0
        checked_options = []
        guesses = []
        
        letter_streak = 0
        for letter in letters:
            letter[3] = True
        
        return

    word = answers[random_index]
    
    #Events
    for event in pygame.event.get():
        #On QUIT Event show runQuit
        if event.type == pygame.QUIT:
            runQuit()
        #Mouse Click Event
        if event.type == pygame.MOUSEBUTTONDOWN:
            m_x,m_y = pygame.mouse.get_pos()
            #If clicked Cross then show runQuit
            if hovers( cross, cross_x, cross_y):
                runQuit()
            #Check if a letter is clicked and add it to guesses
            for letter in letters:
                x,y,ltr,visible = letter
                ltr_distance = math.sqrt((x - m_x)**2+(y - m_y)**2)
                if ltr_distance <= RADIUS and visible:
                    letter[3] = False
                    letterInput(ltr)
        #Key Pressed Event
        if event.type == pygame.KEYDOWN:
            key = pygame.key.name(event.key)
            key = key.upper()
            for letter in letters:
                ltr,visible=letter[2],letter[3]
                if key == ltr and visible:
                    letter[3] = False
                    letterInput(ltr)
                    
    #Draw background and man
    screen.fill(L_GREY)
    screen.blit(bg,(0,0))
    try:
        screen.blit(man_images[man_state],(10,20))
    except IndexError:
        print("Got IndexError for 'man_images[man_state]'\nman_state set to 6 to avoid errors")
        man_state=6
        screen.blit(man_images[man_state],(10,20))
    
    
    #Display Question Image and  Available Letters
    screen.blit(questions[random_index],(410,0))        
    display_word = ""
    drawLetters()
    
    #Display formed word
    show_blanks = True
    order_matters = False
    if level == 1:
        pass
    elif level == 2:
        if man_state >= 2:
            show_blanks = True
        else:
            show_blanks = False
    elif level == 3:
        if man_state >= 4:
            show_blanks = True
        else:
            show_blanks = False
    elif level == 4:
        order_matters = True
        show_blanks = True
    elif level == 5:
        order_matters = True
        if man_state >= 2:
            show_blanks = True
        else:
            show_blanks = False

    if order_matters:
        for letter in guesses:
            display_word += letter + " "
        if show_blanks:
            display_word += (len(word) -len(guesses)) * "_ "
    else:
        for letter in word:
            if letter in guesses:
                display_word += letter + " "
            elif show_blanks:
                display_word += "_ "

        
    text = WORD_FONT.render(display_word,1,WHITE)
    screen.blit(text,(WIDTH*0.75 - text.get_width()/2,400))

    #Display Score
    scoretext = HUD_FONT.render('SCORE: '+str(total_score),1,L_BLUE)
    screen.blit(scoretext,(50,8))

    #Display Lives
    text = HUD_FONT.render('LIVES: '+str(lives),1,L_BLUE)
    screen.blit(text,(250,8))

    #Display Levels
    text = HUD_FONT.render('LEVEL: '+str(level),1,L_BLUE)
    screen.blit(text,(450,8))
        

    #Display Score Change
    if score_change_info[2]: #has a 'right'/'wrong' value when score was changed recently
        score_change_info[1] = datetime.datetime.now()
        #sc_time is time passed in seconds since score changed i.e guess input 
        sc_time = (score_change_info[1] - score_change_info[0]).total_seconds()
        #Below condition checks if less than 3 second has passed since last guess input
        if sc_time < 3:
            if score_change_info[2] == 'right': #if last guess correct
                text = SCORE_FONT.render('+'+str(score_change)+ ' ' + score_change_info[3],1,GREEN)
                #Below statement reduces opacity of score_change text when 2 < sc_time < 3
                text.set_alpha(255 - 255*(sc_time-2))
                screen.blit(text,(WIDTH*0.75 - text.get_width()/2,470))
            elif score_change_info[2] == 'wrong': #if last guess wrong
                text = SCORE_FONT.render((str(score_change) if total_score>0 else '')+ ' ' + score_change_info[3],1,RED)
                #Below statement reduces opacity of score_change text when 2 < sc_time < 3
                text.set_alpha(255 - 255*(sc_time-2))
                screen.blit(text,(WIDTH*0.75 - text.get_width()/2,470))
            else: #3rd parameter of score_change_info is not 'right'/'wrong'/None
                print("Third parameter is wrong in score_change_info")
        else:
            score_change_info = [0,0,0,'']
    

    
    drawCross()


#----------Scene LEADERBOARD----------#
def runLeaderboard():
    global hs_records
    global player_inserted
    global player_record
    global player_registered
    global scene
   
    screen.fill(L_GREY)
    screen.blit(bg,(0,0))
    screen.blit(board1,(WIDTH/2 - board1.get_width()/2,20))
    text = PARA_FONT.render('LEADERBOARD',1,ORANGE)
    screen.blit(text,(WIDTH/2 - text.get_width()/2,37))
    if not player_registered:
        text = INFO_FONT.render('Please type in your name and press ENTER',1,ORANGE)
        screen.blit(text,(WIDTH/2 - text.get_width()/2,100))
    
    #INPUT NEW RECORD
    #Flag player_inserted checks if player's record inserted in hs_records.
    #For first iteration of runLeaderboard(), player_inserted is False
    if player_inserted == False:
        player_record = hs_record('',total_score)
        hs_records.append(player_record)
        player_inserted = True
    else:
        for event in pygame.event.get():
            #On QUIT Event runQuit
            if event.type == pygame.QUIT:
                runQuit()

            #below block executes when player views leaderboard without entry
            #player_registered is True eventhough player is not included in leaderboard
            #Flag player_registered checks if player has finished entering name and pressed ENTER key
            if player_registered:
                if event.type == pygame.MOUSEBUTTONDOWN and hovers( ok_btn, ok_btn_x, ok_btn_y):
                    scene='OPTIONS'
                    return
                if event.type == pygame.KEYDOWN:
                    print('keydown')
                    if pygame.key.name(event.key).upper() == 'RETURN':
                        scene='OPTIONS'
                        return
            else:
                if event.type == pygame.MOUSEBUTTONDOWN and hovers( ok_btn, ok_btn_x, ok_btn_y) and len(player_record.name)>0:
                    print('writing to hs.sav...')
                    player_registered = True
                    player_record.name = player_record.name.strip()
                    with open(os.path.join(path,'data/hs.sav'),'w',encoding='utf-8') as hsfile:
                        print('sav path:',os.path.join(path,'data/hs.sav'))
                        for record in hs_records:
                            score = str(record.score)
                            score = '0'*(6-len(score)) + score
                            name = record.name
                            ctext = encrypt.string(score+name,'ayush')
                            hsfile.write('\n'+ctext)
                    scene='OPTIONS'
                    return
                if event.type == pygame.KEYDOWN:
                    key = pygame.key.name(event.key)
                    key = key.upper()
                    
                    if key == "RETURN" and len(player_record.name) > 0:
                        print('writing to hs.sav...')
                        player_registered = True
                        player_record.name = player_record.name.strip()
                        with open(os.path.join(path,'data/hs.sav'),'w',encoding='utf-8') as hsfile:
                            print('sav path:',os.path.join(path,'data/hs.sav'))
                            for record in hs_records:
                                score = str(record.score)
                                score = '0'*(6-len(score)) + score
                                name = record.name
                                ctext = encrypt.string(score+name,'ayush')
                                hsfile.write('\n'+ctext)
                        scene='OPTIONS'
                        return
                    
                    elif key == "BACKSPACE":
                        if len(player_record.name) > 0:
                            player_record.name = player_record.name[:-1]
                    elif key == "SPACE":
                        key = ' '
                    
                        
                    if len(key) == 1 and len(player_record.name) == 0:
                        #Take only letters for first character of player name
                        if 65 <= ord(key) <= 90:
                            player_record.name += key
                    elif len(key) == 1 and len(player_record.name) < 8:
                        if 65 <= ord(key) <= 90 or 48 <= ord(key) <= 57 or ord(key) == 32:
                            player_record.name += key
            
            #If clicks Cross then runQuit
            if event.type == pygame.MOUSEBUTTONDOWN and hovers( cross, cross_x, cross_y):
                    runQuit()

        if not player_registered:
            hs_records.pop(player_record.position - 1)
            hs_records.append(player_record)
            player_inserted = True

    #Sort hs_records based on record.score
    
    hs_records = sortRecords(hs_records)

    #if hs_records has more than 5 elements, then trim the ones at the end to get only top 5
    if len(hs_records)>5:
        hs_records = hs_records[ :5]

    
    #Draw records: position,name,score
    for i,record in enumerate(hs_records):
        if i==0:
            color=GOLDEN
        elif i==1:
            color=SILVER
        elif i==2:
            color=D_ORANGE
        else:
            color=BLACK
            
        textobj = LEADER_FONT.render(str(record.position),1,color)
        screen.blit(textobj,(150,leader_starty + 10 + i*leader_gap))

        textobj = LEADER_FONT.render(record.name,1,color)
        screen.blit(textobj,(200,leader_starty + 10 + i*leader_gap))
 
        textobj = LEADER_FONT.render(str(record.score),1,color)
        screen.blit(textobj,(500,leader_starty + 10 + i*leader_gap))

    #In case of no records, display a text
    if len(hs_records) == 0:
        textobj = INFO_FONT.render(str('No records registered yet.'),1,D_ORANGE)
        screen.blit(textobj,(WIDTH/2 - textobj.get_width()/2,HEIGHT/2 - 30))
        textobj = INFO_FONT.render(str('Be the first one to claim a spot here!'),1,D_ORANGE)
        screen.blit(textobj,(WIDTH/2 - textobj.get_width()/2,HEIGHT/2))
    
    #Draw ok button
    if len(player_record.name) > 0:
        m_x,m_y = pygame.mouse.get_pos()
        if hovers( ok_btn, ok_btn_x, ok_btn_y):
            screen.blit(ok_btn_green,(ok_btn_x,ok_btn_y))
        else:
            screen.blit(ok_btn,(ok_btn_x,ok_btn_y)) 
    else:
        screen.blit(ok_btn_grey,(ok_btn_x,ok_btn_y))

    #Draw Cross Button
    drawCross()

    pygame.display.update()


#----------View LEADERBOARD----------# 
def viewLeaderboard():
    global scene
    global player_registered
    global player_inserted
    scene='LEADERBOARD'
    player_registered = True
    player_inserted = True
    while scene=='LEADERBOARD':
        runLeaderboard()

#----------Scene QUIT----------#
def runQuit():
    global scene
    global running
    prev_scene = scene
    scene = "QUIT"
    screenCover()
    while scene == "QUIT":
        screen.blit(board2,(WIDTH/2 - board2.get_width()/2,HEIGHT/2 - board2.get_height()/2))
        text = PARA_FONT.render('EXIT?',1,ORANGE)
        screen.blit(text,(WIDTH/2 - text.get_width()/2.5,HEIGHT/2 - board2.get_height()/4))
        
        if hovers(yes_btn, yes_btn_x, yes_btn_y):
            screen.blit(yes_btn_hover,(yes_btn_x,yes_btn_y)) 
        else:
            screen.blit(yes_btn,(yes_btn_x,yes_btn_y))
        
        if hovers(no_btn, no_btn_x, no_btn_y):
            screen.blit(no_btn_hover,(no_btn_x,no_btn_y))
        else:
            screen.blit(no_btn,(no_btn_x,no_btn_y))
        
        pygame.display.update()
        for event in pygame.event.get():
            #Mouse Click Event
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x,m_y = pygame.mouse.get_pos()
                #If clicks yes then quit
                if hovers(yes_btn, yes_btn_x, yes_btn_y):
                    global running
                    running = False
                    scene = ""
                elif hovers(no_btn, no_btn_x, no_btn_y):
                    scene = prev_scene
    
    
#----------------------------------------#
#----------------------------------------#
#***************LOAD DATA***************#
#----------------------------------------#
#----------------------------------------#

#Man States
man_images = []
try:
    for i in range(7):
        image = loadImage("man"+str(i)+".png")
        man_images.append(image)
except:
    error("Hangman Images Not Found","Error when loading images for hangman from 'data' folder")

#Sprites
bg = loadImage("BG.png",(WIDTH,HEIGHT))

#Cross Button
cross = loadImage("cross_blue.png",(50,50))
cross_red = loadImage("cross_red.png",(50,50))
cross_x = WIDTH - cross.get_width() - 10
cross_y = 10

#Boards
board1 = loadImage("board01.png",(667,460))
board2 = loadImage("board02.png",(415,240))

#Start Button
start_btn = loadImage("start_blue.png",(150,70))
start_btn_green = loadImage("start_green.png",(150,70))
start_btn_grey = loadImage("start_grey.png",(150,70))
start_btn_x = WIDTH/2 - start_btn.get_width()/2
start_btn_y = 300

#Yes Button
yes_btn = loadImage("yes_blue.png",(150,70))
yes_btn_hover = loadImage("yes_red.png",(150,70))
yes_btn_x = WIDTH/2 - board2.get_width()/2 + 40
yes_btn_y = HEIGHT/2

#No Button
no_btn = loadImage("no_blue.png",(150,70))
no_btn_hover = loadImage("no_green.png",(150,70))
no_btn_x = WIDTH/2 + 40
no_btn_y = HEIGHT/2

#OK Button
ok_btn = loadImage("ok_blue.png",(150,70))
ok_btn_green = loadImage("ok_green.png",(150,70))
ok_btn_grey = loadImage("ok_grey.png",(150,70))
ok_btn_x = WIDTH/2 - ok_btn.get_width()/2
ok_btn_y = 330

#Leaderboard Button
lb = loadImage("lb_blue.png",(50,50))
lb_green = loadImage("lb_green.png",(50,50))
lb_x = WIDTH - lb.get_width() - 10
lb_y = 70

#Load Topic Names and Checkboxes
options = []
topics_file = open(os.path.join(path,'data/topics.cfg'),'r')
for topic in topics_file.readlines()[1:-1]:
    options.append(topic[:-1])
topics_file.close()
for i in range(len(options)):
    chkboxes.append(gui_checkbox.Checkbox(screen, 500, options_starty+i*options_gap, length=30))

#Load Leaderboard
hs_records = []

player_record = hs_record('player',1000)

#Load top 5 highscores from 'hs.sav'. If any error occurs then rewrite 'hs.sav' as an empty file
try:
    with open(os.path.join(path,'data/hs.sav'),'r',encoding='utf-8') as hsfile:
        isempty = True
        print('hs reading')
        for line in hsfile.read().splitlines():
            if len(line) == 0:
                continue
            isempty = False
            print(line)
            line = decrypt.string(line,'ayush')
            rposition = line[0]
            rscore = int(line[:6])
            rname = line[6:]
            record = hs_record(rname,rscore)
            print(record.isWorking())
            print('hs_record:',record.position,record.name,record.score)
            hs_records.append(record)
        if isempty:
            raise ZeroDivisionError
except ZeroDivisionError:
    safe_error('hs.sav is empty','hs.sav will be overwritten as an empty file')
    with open(os.path.join(path,'data/hs.sav'),'w',encoding='utf-8') as hsfile:
        hsfile.write('')
except Exception as e:
    safe_error('Cannot read the file hs.sav','hs.sav will be overwritten as an empty file')
    with open(os.path.join(path,'data/hs.sav'),'w',encoding='utf-8') as hsfile:
        print(e)
        hsfile.write('')


#options = ['Non Verbal','Real Objects','Riddles','Science']
    
#----------------------------------------#
#----------------------------------------#
#***************GAME LOOP***************#
#----------------------------------------#
#----------------------------------------#
runIntro()
dummieKey()
try:
    while running:    
        if scene == "OPTIONS":
            runOptions()
        elif scene == "GAME":
            runGame()

        pygame.display.update()

        if lives == 0:
            drawMessage("GAME OVER!",2)
            game_over = 'Out of guesses'
            
        if game_over:
            print('Game over! Reason:',game_over)
            isHs = False
            if len(hs_records) < leaderboard_limit:
                if total_score > 0:
                    isHs=True
            elif total_score > hs_records[-1].score:
                isHs=True
            
            if isHs:
                drawMessage("You made it to HIGHSCORES!",2)
                player_registered = False
                player_inserted = False
                scene = 'LEADERBOARD'
                dummieKey()
                while scene == 'LEADERBOARD':
                    runLeaderboard()
            
            dummieKey()
            scene = "OPTIONS"
            game_over_reset()
            game_over = False
        
        won = True
        if order_matters:
            if word != ''.join(guesses):
                won = False       
        else:
            for letter in word:
                if letter not in guesses:
                    won = False
                    break
        if won:
            game_state = 2
            pygame.time.delay(2000)
            words_guessed[0] += 1
            words_guessed[1] += 1
            if words_guessed[0] in level_point:
                drawMessage('Level Complete',2)
            dummieKey()  

        if man_state == 6:
            game_state = 3
            pygame.time.delay(3000)
            lives -= 1
            words_guessed[1] += 1
            dummieKey()

        if words_guessed[0] < level_point[0]:
            #1 Show blanks, letter order does not matter
            level = 1
        elif words_guessed[0] < level_point[1]:
            #2 Show blanks only after 2 wrong guesses, letter order does not matter
            if level != 2:
                showInfo('LEVEL 2',level_info[2])
            level = 2
        elif words_guessed[0] < level_point[2]:
            #3 Show blanks only after 5 wrong guesses, letter order does not matter
            if level != 3:
                showInfo('LEVEL 3',level_info[3])
            level = 3
        elif words_guessed[0] < level_point[3]:
            #4 Show blanks, letter order matters
            if level != 4:
                showInfo('LEVEL 4',level_info[4])
            level = 4
        else:
            #5 Show blanks only after 2 wrong guesses, letter order matters
            if level != 5:
                showInfo('LEVEL 5',level_info[5])
            level = 5

        
except Exception as unhandled_error:
    error('Error!','Unhandled Exception: '+str(unhandled_error))
#***************END GAME LOOP***************#
pygame.quit()
