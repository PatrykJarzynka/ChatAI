import { beforeEach, describe, expect, jest, test } from '@jest/globals';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ChatHistory } from './chat-history.component';
import { ChatHistory as ChatHistoryType } from '../../../../../types/ChatHistory';
import { ChatHistoryService } from '../../../../../services/ChatHistoryService';
import { MOCK_CHAT_HISTORY, MOCKED_CHAT_RESPONSE, MOCKED_INITIAL_CHAT } from '../../../../../utils/mockedData';
import { ChatService } from '../../../../../services/ChatService';
import useParser from '../../../../../composables/useParser';


jest.mock('../../../../../composables/useParser', () => {
    const actualUseParser = jest.requireActual('../../../../../composables/useParser') as any;

    return {
      ...actualUseParser.default,
      parseChatResponseToChat: jest.fn(() => MOCKED_INITIAL_CHAT)
    };
  }
);


describe('ChatHistory', () => {
  let component: ChatHistory;
  let fixture: ComponentFixture<ChatHistory>;
  let chatHistoryService: ChatHistoryService;
  let chatService: ChatService;


  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [ChatHistory],
      providers: [ChatHistoryService, ChatService],
    });

    chatService = TestBed.inject(ChatService);
    chatHistoryService = TestBed.inject(ChatHistoryService);
    jest.spyOn(chatHistoryService, 'fetchChatHistories').mockResolvedValue([]);

    fixture = TestBed.createComponent(ChatHistory);
    component = fixture.componentInstance;

    fixture.detectChanges();
  });

  function checkRenderedList(chatHistoriesArray: ChatHistoryType[]) {
    const renderedChatHistories: HTMLDivElement[] = fixture.nativeElement.querySelectorAll('.list-item');

    expect(renderedChatHistories.length).toBe(chatHistoriesArray.length);

    renderedChatHistories.forEach((renderedChatHistory, index) => {
      const chatHistoryItem = renderedChatHistory.querySelector('.chat-history-item');
      const title = chatHistoryItem?.querySelector('p');
      expect(title?.textContent).toBe(chatHistoriesArray[index].title);
    });
  }

  test('should display no data info', () => {
    const noDataWrapper = fixture.nativeElement.querySelector('.default-item');
    const label = noDataWrapper.querySelector('p');

    expect(chatHistoryService.getAllChatHistories().size).toBe(0);
    expect(label.textContent).toBe('No messages.');
  });

  test('should render chat histories', () => {
    const chatHistoriesArray = [MOCK_CHAT_HISTORY];

    chatHistoryService.setChatHistories(chatHistoriesArray);

    fixture.detectChanges();

    checkRenderedList(chatHistoriesArray);
  });

  test('should render new chat history after adding it to the list', () => {

    const chatHistoriesArray = [MOCK_CHAT_HISTORY];

    chatHistoryService.setChatHistories(chatHistoriesArray);

    fixture.detectChanges();

    chatHistoryService.updateChatHistory({
      title: 'TestTitle',
      id: 1234
    });

    fixture.detectChanges();

    checkRenderedList(Array.from(component.chatHistories()));
  });

  test('should fetch chat histories on init', () => {
    jest.spyOn(chatHistoryService, 'fetchChatHistories');

    expect(chatHistoryService.fetchChatHistories).toBeCalled();
  });

  test('should update current chat after click on chat history item', async () => {
    jest.spyOn(component, 'updateCurrentChat');
    jest.spyOn(chatService, 'fetchChatByChatId').mockResolvedValue(MOCKED_CHAT_RESPONSE);
    jest.spyOn(chatService, 'setCurrentChat');

    const chatHistoriesArray = [MOCK_CHAT_HISTORY];

    chatHistoryService.setChatHistories(chatHistoriesArray);

    fixture.detectChanges();

    const chatHistoryItem: HTMLDivElement = fixture.nativeElement.querySelectorAll('.list-item')[0];

    chatHistoryItem.click();

    await fixture.whenStable();

    expect(component.updateCurrentChat).toHaveBeenCalledWith(MOCK_CHAT_HISTORY.id);
    expect(chatService.fetchChatByChatId).toHaveBeenCalledWith(MOCK_CHAT_HISTORY.id);
    expect(useParser.parseChatResponseToChat).toHaveBeenCalledWith(MOCKED_CHAT_RESPONSE);
    expect(chatService.setCurrentChat).toHaveBeenCalledWith(MOCKED_INITIAL_CHAT);
  });

  test('should set chat history as selected after click', () => {
    jest.spyOn(chatHistoryService, 'fetchChatHistories');

    expect(chatHistoryService.fetchChatHistories).toBeCalled();
  });
});
