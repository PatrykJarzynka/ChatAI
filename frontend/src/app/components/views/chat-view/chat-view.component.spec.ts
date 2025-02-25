import { beforeEach, describe, expect, jest, test } from '@jest/globals';
import { ChatService } from '@services/ChatService';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import {
  MOCK_CHAT_HISTORY,
  MOCK_CHAT_WITH_ITEMS,
  MOCK_QUERY,
  MOCK_USER,
  MOCKED_INITIAL_CHAT
} from '@utils/mockedData';
import { By } from '@angular/platform-browser';
import { ChatHistoryService } from '@services/ChatHistoryService';
import useChatActions from '@composables/useChatActions';
import { Chat } from 'appTypes/Chat';
import { StatusType } from '@enums/StatusType';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { ChatView } from './chat-view.component';
import { Router } from '@angular/router';
import { UserService } from '@services/UserService';
import { AppSidebar } from '@components/core/app-sidebar/app-sidebar.component';
import { ChatActions } from '@components/features/chat/chat-actions/chat-actions.component';
import { AuthService } from '@services/AuthService';


jest.mock('@composables/useChatActions', () => (
  jest.fn(() => ( {
    handleFetchingBotMessage: jest.fn(),
  } ))
));

describe('appComponent', () => {
  let router: Router;
  let component: ChatView;
  let fixture: ComponentFixture<ChatView>;
  let chatService: ChatService;
  let chatHistoryService: ChatHistoryService;
  let userService: UserService;
  let authService: AuthService;
  let mockHandleFetchingBotMessage: jest.Mock;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [ChatView, AppSidebar, ChatActions, BrowserAnimationsModule],
      providers: [ChatService],
    });

    chatService = TestBed.inject(ChatService);
    chatHistoryService = TestBed.inject(ChatHistoryService);
    userService = TestBed.inject(UserService);
    authService = TestBed.inject(AuthService);
    router = TestBed.inject(Router);

    jest.spyOn(chatHistoryService, 'fetchChatHistories').mockResolvedValue([MOCK_CHAT_HISTORY]);
    mockHandleFetchingBotMessage = jest.fn();
    ( useChatActions as jest.Mock ).mockReturnValue({
      handleFetchingBotMessage: mockHandleFetchingBotMessage,
    });


    fixture = TestBed.createComponent(ChatView);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  describe('togglePanelVisibility', () => {
    test('should toggle panel visibility when panel emits toggle event', async () => {
      const panelButton = fixture.nativeElement.querySelector('.sidebar-toggle-button');
      panelButton.click();

      fixture.detectChanges();

      await fixture.whenStable();

      expect(component.panelVisibility()).toEqual(false);
    });
  });

  describe('toggleBotFail', () => {
    test('should update bot fail state', () => {
      const panel = fixture.nativeElement.querySelector('.sidebar-wrapper');
      const panelCheckbox = panel.querySelector('.mdc-checkbox__native-control');

      panelCheckbox.click();

      expect(component.shouldFail()).toEqual(true);
    });
  });

  describe('startNewChat', () => {
    let panel: HTMLDivElement;
    let panelNewChatButton: HTMLButtonElement | null;

    beforeEach(() => {
      jest.spyOn(component, 'startNewChat');
      jest.spyOn(chatService, 'startNewChat');

      panel = fixture.nativeElement.querySelector('.sidebar-wrapper');
      panelNewChatButton = panel.querySelector('.new-chat-button');
    });

    test('should start new chat when panel emits new chat event', async () => {
      jest.spyOn(chatService, 'fetchNewChat').mockResolvedValue(MOCK_CHAT_WITH_ITEMS);
      chatService.setCurrentChat(MOCK_CHAT_WITH_ITEMS);

      panelNewChatButton?.click();

      expect(component.startNewChat).toHaveBeenCalled();
      expect(chatService.startNewChat).toHaveBeenCalled();
    });

    test('should not start new chat when panel emits new chat event', async () => {
      chatService.setCurrentChat(MOCKED_INITIAL_CHAT);

      if (panelNewChatButton) {
        panelNewChatButton.click();
      }

      expect(component.startNewChat).toHaveBeenCalled();
      expect(chatService.startNewChat).not.toHaveBeenCalled();
    });
  });

  describe('onUserQuerySend', () => {

    beforeEach(() => {
      jest.spyOn(component, 'onUserQuerySend');
      jest.spyOn(chatService, 'startNewChat');
      jest.spyOn(chatService, 'createAndAddChatItemTemplate');
      jest.spyOn(chatService, 'fetchNewChat').mockResolvedValue(MOCKED_INITIAL_CHAT);
    });

    test('should create new chat, create chat item and update bot message on chat action event', async () => {
      const chatActions = fixture.debugElement.query(By.css('.chat-actions'));
      chatActions.componentInstance.querySend.emit(MOCK_QUERY);

      await fixture.whenStable();
      expect(component.onUserQuerySend).toHaveBeenCalledWith(MOCK_QUERY);
      expect(chatService.startNewChat).toHaveBeenCalled();
      await fixture.whenStable();
      expect(chatService.createAndAddChatItemTemplate).toHaveBeenCalledWith(MOCK_QUERY);
      expect(mockHandleFetchingBotMessage).toHaveBeenCalledWith(MOCK_QUERY, component.shouldFail());
    });

    test('should not react on enter key press', () => {
      const chatActions = fixture.debugElement.query(By.css('.chat-actions'));
      const input = chatActions.nativeElement.querySelector('input');

      input.dispatchEvent(new KeyboardEvent('keydown', {
        key: 'Enter'
      }));

      expect(component.onUserQuerySend).not.toHaveBeenCalled();
    });

    test('should not react on button click', () => {
      const chatActions = fixture.debugElement.query(By.css('.chat-actions'));
      const sendButton = chatActions.nativeElement.querySelector('.send-button');

      sendButton.click();

      expect(component.onUserQuerySend).not.toHaveBeenCalled();
    });
  });

  describe('refetchBotMessage', () => {
    test('should refetch bot message', () => {
      jest.spyOn(component, 'refetchBotMessage');
      jest.spyOn(chatService, 'updateLatestBotMessageDataProperty');

      const MOCK_CHAT_WITH_FAILED_BOT_MESSAGE: Chat = {
        id: 123,
        chatItems: [
          {
            userMessage: MOCK_QUERY,
            botMessageData: {
              text: 'Test',
              status: StatusType.Failed
            }
          }
        ]
      };

      chatService.setCurrentChat(MOCK_CHAT_WITH_FAILED_BOT_MESSAGE);
      const chatWindow = fixture.nativeElement.querySelector('.chat-window');
      fixture.detectChanges();
      const refetchButton = chatWindow.querySelector('.error-button');

      refetchButton.click();

      expect(component.refetchBotMessage).toHaveBeenCalledWith(MOCK_QUERY);
      expect(chatService.updateLatestBotMessageDataProperty).toHaveBeenCalledWith('status', StatusType.Pending);
      expect(mockHandleFetchingBotMessage).toHaveBeenCalledWith(MOCK_QUERY, component.shouldFail());

    });
  });

  describe('init', () => {

    test('should redirect to auth page when access token is not saved in local storage', () => {
      jest.spyOn(router, 'navigate');

      component.ngOnInit();

      expect(router.navigate).toHaveBeenCalledWith(['/']);
    });

    test('should redirect to auth page when access token is invalid', async () => {
      localStorage.setItem('token', 'invalidToken');
      jest.spyOn(router, 'navigate');

      jest.spyOn(authService, 'verifyToken').mockRejectedValue('Invalid token.');
      await component.ngOnInit();

      expect(router.navigate).toHaveBeenCalledWith(['/']);
    });

    test('should get user and set token', async () => {
      localStorage.setItem('token', 'mockToken');
      jest.spyOn(userService, 'fetchUser').mockResolvedValue(MOCK_USER);
      jest.spyOn(authService, 'handleSettingRefreshTokenInterval').mockImplementation(() => {
      });
      jest.spyOn(authService, 'verifyToken').mockResolvedValue({ accessToken: 'verifiedToken', tokenType: 'bearer' });
      await component.ngOnInit();

      const currentUser = userService.getCurrentUser();

      expect(userService.fetchUser).toHaveBeenCalled();
      expect(authService.handleSettingRefreshTokenInterval).toHaveBeenCalled();
      expect(authService.verifyToken).toHaveBeenCalled();
      expect(currentUser()).toEqual(MOCK_USER);
    });
  });

  describe('logout', () => {
    test('should logout user on button click and remove refresh token interval', async () => {
      localStorage.setItem('token', 'mockToken');
      authService.refreshTokenCallInterval = 1;
      jest.spyOn(component, 'onLogoutButtonClick');
      jest.spyOn(router, 'navigate');
      jest.spyOn(global, 'clearInterval');

      const profileButton = fixture.nativeElement.querySelector('.profile-button');

      await profileButton.click();

      fixture.detectChanges();

      const logoutButton = fixture.debugElement.query(By.css('.logout-button'));

      logoutButton.nativeElement.click();

      const token = localStorage.getItem('token');

      expect(global.clearInterval).toHaveBeenCalled();
      expect(component.onLogoutButtonClick).toHaveBeenCalled();
      expect(token).toBeNull();
      expect(router.navigate).toHaveBeenCalledWith(['/']);
    });
  });
});
