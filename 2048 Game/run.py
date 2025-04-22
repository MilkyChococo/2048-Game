import pygame
import time
fps=60
#Khởi tạo Pygame
pygame.init()
#Tải nhạc nền lên và chơi nhạc
pygame.mixer.music.load("background_music_1.mp3")
pygame.mixer.music.play()
#Khởi tạo chiều dài và rộng của Menu
width=500
height=500
#Trình chiếu Menu
pygame.display.set_mode((width,height))
#Tải hình nền Menu
background=pygame.transform.scale(pygame.image.load('background_menu.png'),(500,200))
win=pygame.display.set_mode((width,height))
win.fill((0,120,215,255))
win.blit(background,(0,0))
#Sử dụng Font chữ Cambria
font=pygame.font.SysFont('cambria',30)
#Khởi tạo hiệu ứng khi ấn vào Button
click=pygame.mixer.Sound("click_button.mp3")
#Tạo đường dẫn đến file Game4x4 thông qua class button4x4
class button4x4:
    def __init__(self,image,x_pos,y_pos,text_input):
        self.image=image
        self.x=x_pos
        self.y=y_pos
        self.rect=self.image.get_rect(center=(self.x,self.y))
        self.text=text_input
        self.txt=font.render(self.text,True,"white")
        self.text_rect=self.txt.get_rect(center=(self.x,self.y))
    def update(self):
        win.blit(self.image,self.rect)
        win.blit(self.txt,self.text_rect)
    #Kiểm tra nút có được ấn hay chưa, nếu ấn thì sẽ dẫn sang Game 4x4
    def checkForInput(self,pos):
        if pos[0] in range(self.rect.left,self.rect.right) and pos[1] in range(self.rect.top,self.rect.bottom):
            click.play()
            pygame.mixer.music.stop()
            time.sleep(1)
            from Game4x4 import Game2048
            game = Game2048()
            game.run_game()
    #Khi lướt qua nút thì nút sẽ đổi màu
    def changeColor(self, pos):
        if pos[0] in range(self.rect.left, self.rect.right) and pos[1] in range(self.rect.top, self.rect.bottom): self.txt = font.render(self.text, True, "black") 
        else: self.txt = font.render(self.text, True, (238, 228, 218))
#Tạo đường dẫn đến file Game6x6 thông qua class button6x6
class button6x6:
    def __init__(self,image,x_pos,y_pos,text_input):
        self.image=image
        self.x=x_pos
        self.y=y_pos
        self.rect=self.image.get_rect(center=(self.x,self.y))
        self.text=text_input
        self.txt=font.render(self.text,True,"white")
        self.text_rect=self.txt.get_rect(center=(self.x,self.y))
    def update(self):
        win.blit(self.image,self.rect)
        win.blit(self.txt,self.text_rect)
    #Kiểm tra nút có được ấn hay chưa, nếu ấn thì sẽ dẫn sang Game6x6
    def checkForInput(self,pos):
        if pos[0] in range(self.rect.left,self.rect.right) and pos[1] in range(self.rect.top,self.rect.bottom):
            click.play()
            pygame.mixer.music.stop()
            time.sleep(1)
            from Game6x6 import Game2048
            game = Game2048()
            game.run_game()
    #Khi lướt qua nút thì nút sẽ đổi màu
    def changeColor(self, pos):
        if pos[0] in range(self.rect.left, self.rect.right) and pos[1] in range(self.rect.top, self.rect.bottom): self.txt = font.render(self.text, True, "black") 
        else: self.txt = font.render(self.text, True, (238, 228, 218))
        
class button8x8:
    def __init__(self,image,x_pos,y_pos,text_input):
        self.image=image
        self.x=x_pos
        self.y=y_pos
        self.rect=self.image.get_rect(center=(self.x,self.y))
        self.text=text_input
        self.txt=font.render(self.text,True,"white")
        self.text_rect=self.txt.get_rect(center=(self.x,self.y))
    def update(self):
        win.blit(self.image,self.rect)
        win.blit(self.txt,self.text_rect)
    #Kiểm tra nút có được ấn hay chưa, nếu ấn thì sẽ dẫn sang Game8x8
    def checkForInput(self,pos):
        if pos[0] in range(self.rect.left,self.rect.right) and pos[1] in range(self.rect.top,self.rect.bottom):
            click.play()
            pygame.mixer.music.stop()
            time.sleep(1)
            from Game8x8 import Game2048
            game = Game2048()
            game.run_game()
    #Khi lướt qua nút thì nút sẽ đổi màu
    def changeColor(self, pos):
        if pos[0] in range(self.rect.left, self.rect.right) and pos[1] in range(self.rect.top, self.rect.bottom): self.txt = font.render(self.text, True, "black") 
        else: self.txt = font.render(self.text, True, (238, 228, 218))
#Tạo hình cho các button
button_surface = pygame.image.load("button_menu.png")
button_surface = pygame.transform.scale(button_surface, (150, 50))
#Tạo các button
button4x4 = button4x4(button_surface, 250, 250, "Game 4x4")
button6x6 = button6x6(button_surface, 250, 350, "Game 6x6")
button8x8 = button8x8(button_surface, 250, 450, "Game 8x8")
#Chạy chương trình
while True:
    #Lặp lại bài nhạc nền khi nhạc kết thúc
    if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            exit()
        #Kiểm tra nút nào được ấn
        if event.type == pygame.MOUSEBUTTONDOWN: 
            button4x4.checkForInput(pygame.mouse.get_pos())
            button6x6.checkForInput(pygame.mouse.get_pos())
            button8x8.checkForInput(pygame.mouse.get_pos())
#Cập nhật trạng thái   
    button4x4.update()
    button4x4.changeColor(pygame.mouse.get_pos())
    button6x6.update()
    button6x6.changeColor(pygame.mouse.get_pos())
    button8x8.update()
    button8x8.changeColor(pygame.mouse.get_pos())
    pygame.display.update()
