import pygame
import random
import copy
class Game2048:
    def __init__(self):
        #Chạy Pygame và Nhạc trong Pygame
        pygame.init()
        pygame.mixer.init()
        #Tải nhạc nền và bật nhạc
        pygame.mixer.music.load("background_music.mp3")
        pygame.mixer.music.play()
        #Hiệu ứng âm thanh khi không thể di chuyển các khối ở rìa
        self.block=pygame.mixer.Sound("block.mp3")
        #Dãy các trạng thái bảng trước đó
        self.previous_states = []
        #Tải hình nút Reset
        self.reset_pic=pygame.transform.scale(pygame.image.load('button reset.png'),(100,100))
        self.undo_count=2
        #Tải hiệu ứng khi di chuyển các khối
        self.sound = pygame.mixer.Sound("move_sound.mp3")
        #Tải hiệu ứng khi ấn nút
        self.click=pygame.mixer.Sound("click_button.mp3")
        #Tải hiệu ứng khi 2 ô gộp lại với nhau  
        self.ting=pygame.mixer.Sound("ting.mp3")
        #Tạo chiều dài và rộng cho trò chơi
        self.WIDTH = 600
        self.HEIGHT = 700
        #Chạy màn hình với dài rộng ở trên
        self.screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])
        #Đặt tên cho màn chơi
        pygame.display.set_caption('2048')
        self.timer = pygame.time.Clock()
        #Khởi tạo fps chương trình
        self.fps = 60
        #Sử dụng font chữ là freesansbold và 2 kích thước
        self.font = pygame.font.Font('freesansbold.ttf', 24)
        self.font1=pygame.font.Font('freesansbold.ttf',16)
        #Màu sắc
        self.colors = {0: (204, 192, 179),
                       2: (238, 228, 218),
                       4: (237, 224, 200),
                       8: (242, 177, 121),
                       16: (245, 149, 99),
                       32: (246, 124, 95),
                       64: (246, 94, 59),
                       128: (237, 207, 114),
                       256: (237, 204, 97),
                       512: (237, 200, 80),
                       1024: (237, 197, 63),
                       2048: (237, 194, 46),
                       4096: (237, 191, 43),
                       'light text': (249, 246, 242),
                       'dark text': (119, 110, 101),
                       'other': (0, 0, 0),
                       'bg': (187, 173, 160)}
        #Khối ô giá trị trong bản
        self.board_values = [[0 for _ in range(6)] for _ in range(6)]
        self.game_over = False
        self.spawn_new = True
        self.init_count = 0
        self.direction = None
        self.score = 0
        self.init_high = 0
        self.high_score = 0
        #Biến kiểm tra có thể di chuyển được không
        self.edge_spawn_blocked = {'UP': False, 'DOWN': False, 'LEFT': False, 'RIGHT': False}
    #Hàm tạo màn hình Game over khi kết thúc trò chơi
    def draw_over(self):
        pygame.draw.rect(self.screen, 'black', [140, 180, 325, 100], 0, 10)
        game_over_text1 = self.font.render('Game Over!', True, 'white')
        game_over_text2 = self.font.render('Press Enter to Restart', True, 'white')
        self.screen.blit(game_over_text1, (235, 200))
        self.screen.blit(game_over_text2, (175, 240))
    #Các khối ô sẽ di chuyển dựa theo nút ấn UP, DOWN, LEFT, RIGHT
    def take_turn(self, direc, board):
        merged = [[False for _ in range(6)] for _ in range(6)]
        move_made = False

        if direc == 'UP':
            for i in range(1, 6):
                for j in range(6):
                    if board[i][j] != 0:
                        shift = 0
                        for q in range(i):
                            if board[q][j] == 0:
                                shift += 1
                        if shift > 0:
                            board[i - shift][j] = board[i][j]
                            board[i][j] = 0
                            move_made = True
                        if i - shift > 0 and board[i - shift - 1][j] == board[i - shift][j] and not merged[i - shift][j] and not merged[i - shift - 1][j]:
                            board[i - shift - 1][j] *= 2
                            self.ting.play()
                            self.score += board[i - shift - 1][j]
                            board[i - shift][j] = 0
                            merged[i - shift - 1][j] = True
                            move_made = True
            self.edge_spawn_blocked['UP'] = any(board[0][j] != 0 for j in range(6))

        elif direc == 'DOWN':
            for i in range(4, -1, -1):
                for j in range(6):
                    if board[i][j] != 0:
                        shift = 0
                        for q in range(i + 1, 6):
                            if board[q][j] == 0:
                                shift += 1
                        if shift > 0:
                            board[i + shift][j] = board[i][j]
                            board[i][j] = 0
                            move_made = True
                        if i + shift < 5 and board[i + shift + 1][j] == board[i + shift][j] and not merged[i + shift][j] and not merged[i + shift + 1][j]:
                            board[i + shift + 1][j] *= 2
                            self.ting.play()
                            self.score += board[i + shift + 1][j]
                            board[i + shift][j] = 0
                            merged[i + shift + 1][j] = True
                            move_made = True
            self.edge_spawn_blocked['DOWN'] = any(board[5][j] != 0 for j in range(6))

        elif direc == 'LEFT':
            for j in range(1, 6):
                for i in range(6):
                    if board[i][j] != 0:
                        shift = 0
                        for q in range(j):
                            if board[i][q] == 0:
                                shift += 1
                        if shift > 0:
                            board[i][j - shift] = board[i][j]
                            board[i][j] = 0
                            move_made = True
                        if j - shift > 0 and board[i][j - shift - 1] == board[i][j - shift] and not merged[i][j - shift] and not merged[i][j - shift - 1]:
                            board[i][j - shift - 1] *= 2
                            self.ting.play()
                            self.score += board[i][j - shift - 1]
                            board[i][j - shift] = 0
                            merged[i][j - shift - 1] = True
                            move_made = True
            self.edge_spawn_blocked['LEFT'] = any(board[i][0] != 0 for i in range(6))

        elif direc == 'RIGHT':
            for j in range(4, -1, -1):
                for i in range(6):
                    if board[i][j] != 0:
                        shift = 0
                        for q in range(j + 1, 6):
                            if board[i][q] == 0:
                                shift += 1
                        if shift > 0:
                            board[i][j + shift] = board[i][j]
                            board[i][j] = 0
                            move_made = True
                        if j + shift < 5 and board[i][j + shift + 1] == board[i][j + shift] and not merged[i][j + shift] and not merged[i][j + shift + 1]:
                            board[i][j + shift + 1] *= 2
                            self.ting.play()
                            self.score += board[i][j + shift + 1]
                            board[i][j + shift] = 0
                            merged[i][j + shift + 1] = True
                            move_made = True
            self.edge_spawn_blocked['RIGHT'] = any(board[i][5] != 0 for i in range(6))

        return board, move_made
    #Kiểm tra có thể tạo ô mới
    def new_pieces(self, board):
        if self.direction and self.edge_spawn_blocked[self.direction]:
            return board, False

        count = 0
        full = False
        while any(0 in row for row in board) and count < 1:
            row = random.randint(0, 5)
            col = random.randint(0, 5)
            if board[row][col] == 0:
                count += 1
                board[row][col] = 4 if random.randint(1, 10) == 10 else 2
        if count < 1:
            full = True
        return board, full
    #Tạo bảng trò chơi
    def draw_board(self):
        pygame.draw.rect(self.screen, self.colors['bg'], [0, 0, 600, 600], 0, 10)
        score_text = self.font.render(f'Score: {self.score}', True, 'black')
        high_score_text = self.font.render(f'High Score: {self.high_score}', True, 'black')
        self.screen.blit(score_text, (10, 610))
        self.screen.blit(high_score_text, (10, 650))
    #Tạo các ô với các màu tương ứng cho giá trị trên ô
    def draw_pieces(self):
        for i in range(6):
            for j in range(6):
                value = self.board_values[i][j]
                value_color = self.colors['light text'] if value > 8 else self.colors['dark text']
                color = self.colors[value] if value <= 4096 else self.colors['other']
                pygame.draw.rect(self.screen, color, [j * 95 + 20, i * 95 + 20, 75, 75], 0, 5)
                if value > 0:
                    value_len = len(str(value))
                    font = pygame.font.Font('freesansbold.ttf', 48 - (5 * value_len))
                    value_text = font.render(str(value), True, value_color)
                    text_rect = value_text.get_rect(center=(j * 95 + 57, i * 95 + 57))
                    self.screen.blit(value_text, text_rect)
                    pygame.draw.rect(self.screen, 'black', [j * 95 + 20, i * 95 + 20, 75, 75], 2, 5)
    #Kiểm tra xem Game đã kết thúc chưa
    def check_game_over(self):
    # Kiểm tra xem bảng đã đầy chưa
        if any(0 in row for row in self.board_values):
            return False
    # Kiểm tra xem có thể thực hiện thêm bước di chuyển nào không
        for i in range(6):
            for j in range(6):
                current_value = self.board_values[i][j]
                neighbors = []
                if i > 5:
                    neighbors.append(self.board_values[i - 1][j])
                if i < 5:
                    neighbors.append(self.board_values[i + 1][j])
                if j > 5:
                    neighbors.append(self.board_values[i][j - 1])
                if j < 5:
                    neighbors.append(self.board_values[i][j + 1])
                if current_value in neighbors:
                    return False
        return True
    #Lưu nước đi trước đó
    def save_state(self):
        self.previous_states.append((copy.deepcopy(self.board_values), self.score))
    #Hàm quay lại trạng thái trước đó của ô
    def undo(self):
        if self.previous_states and self.undo_count >0:
            self.board_values, self.score = self.previous_states.pop()
            self.undo_count -= 1
    #Xem nút Reset được ấn hay không
    def handle_undo_button(self, pos):
        undo_button_rect = pygame.draw.circle(self.screen, (0, 0, 0), (self.WIDTH - 70, self.HEIGHT - 50), 50)
        if undo_button_rect.collidepoint(pos):
            self.undo()
    #Khởi chạy chương trình
    def run_game(self):
        run = True
        while run:
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play()
            self.timer.tick(self.fps)
            self.screen.fill('gray')
            self.draw_board()
            self.draw_pieces()
            if self.spawn_new or self.init_count < 2:
                self.board_values, self.game_over = self.new_pieces(self.board_values)
                self.spawn_new = False
                self.init_count += 1
            if self.direction:
                self.save_state()   # Lưu trạng thái bảng trước khi di chuyển ô
                self.board_values, move_made = self.take_turn(self.direction, self.board_values)
                if move_made:
                    self.spawn_new = True
                else: 
                    self.block.play()
                    self.previous_states.pop()  # Xóa trạng thái trước khi không di chuyển ô
                self.direction = None
            if self.game_over:
                if self.undo_count>0:
                    pygame.draw.rect(self.screen, 'black', [140, 180, 325, 100], 0, 10)
                    second_chance1 = self.font.render('You can return!', True, 'white')
                    second_chance2 = self.font.render('Click Reset Button', True, 'white')
                    self.screen.blit(second_chance1, (225, 200))
                    self.screen.blit(second_chance2, (195, 240))
                else:
                    self.draw_over()
                    if self.score > self.high_score:
                        self.high_score = self.score
            else:
                self.game_over = self.check_game_over()  # Kiểm tra trạng thái game over
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RETURN:
                        if self.game_over:
                            # Khởi động lại trò chơi khi nhấn phím Enter
                            self.board_values = [[0 for _ in range(6)] for _ in range(6)]
                            self.spawn_new = True
                            self.init_count = 0
                            self.score = 0
                            self.direction = None
                            self.game_over = False
                    elif event.key == pygame.K_UP:
                        self.direction = 'UP'
                    elif event.key == pygame.K_DOWN:
                        self.direction = 'DOWN'
                    elif event.key == pygame.K_LEFT:
                        self.direction = 'LEFT'
                    elif event.key == pygame.K_RIGHT:
                        self.direction = 'RIGHT'
                #Ấn nút Reset
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_undo_button(event.pos)
                    self.click.play()
            #Tạo hình cho nút Reset
            self.screen.blit(self.reset_pic,(self.WIDTH - 120, self.HEIGHT - 100))
            undo_text = self.font1.render(f"Reset: {self.undo_count} ", True, 'black')
            self.screen.blit(undo_text, (self.WIDTH - 100, self.HEIGHT - 55))
            pygame.display.flip()

        pygame.quit()


