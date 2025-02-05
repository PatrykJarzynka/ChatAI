import { beforeEach, describe, expect, jest, test } from '@jest/globals';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ChatHistory } from '../chat-history/chat-history.component';
import { ChatHistory as ChatHistoryType } from '../../../../../types/ChatHistory';
import { ChatHistoryService } from '../../../../../services/ChatHistoryService';
import { MOCK_CHAT_HISTORY } from '../../../../../utils/mockedData';


describe('ChatHistory', () => {
  let component: ChatHistory;
  let fixture: ComponentFixture<ChatHistory>;
  let chatHistoryService: ChatHistoryService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [ChatHistory],
      providers: [ChatHistoryService],
    });

    chatHistoryService = TestBed.inject(ChatHistoryService);
    jest.spyOn(chatHistoryService, 'fetchChatHistories').mockResolvedValue([]);

    fixture = TestBed.createComponent(ChatHistory);
    component = fixture.componentInstance;

    fixture.detectChanges();
  });

  function checkRenderedList(chatHistoriesArray: ChatHistoryType[]) {
    const renderedChatHistories: HTMLDivElement[] = fixture.nativeElement.querySelectorAll('.chat-history-container');

    expect(renderedChatHistories.length).toBe(chatHistoriesArray.length);

    renderedChatHistories.forEach((renderedChatHistory, index) => {
      const title = renderedChatHistory.querySelector('.chat-history-item--title');
      expect(title?.textContent).toBe(chatHistoriesArray[index].title);
    });
  }

  test('should display no data info', () => {
    const label = fixture.nativeElement.querySelector('.no-data-label');

    expect(chatHistoryService.getAllChatHistories().size).toBe(0);
    expect(label.textContent).toBe('No data available');
  });

  test('should render chat histories', () => {
    const chatHistoriesArray = [MOCK_CHAT_HISTORY];

    chatHistoryService.setChatHistories(chatHistoriesArray);

    fixture.detectChanges();

    checkRenderedList(chatHistoriesArray);
  });

  test('should new chat history after adding it to the list', () => {

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

  test('should display default text when there is no histories in the list', () => {
    const noDataLabel = fixture.nativeElement.querySelector('.no-data-label');
    expect(noDataLabel.textContent).toBe('No data available');
  });

});
