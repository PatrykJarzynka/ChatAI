import { StatusType } from '../enums/StatusType';
import { ChatService } from '../services/ChatService';

function useChatActions(chatService: ChatService) {

  async function handleFetchingBotMessage(userQuery:string, chatItemId: string, shouldFail: boolean) {
    const response = await chatService.fetchBotResponse(userQuery,shouldFail);

    if (response) {
      chatService.updateBotMessageDataProperty('text', response, chatItemId);
      chatService.updateBotMessageDataProperty('status', StatusType.Success, chatItemId);
      chatService.updateChatHistory();
    } else {
      chatService.updateBotMessageDataProperty('status', StatusType.Failed, chatItemId);
      chatService.updateChatHistory();
    }
  }

  return {
    handleFetchingBotMessage
  }


}

export default useChatActions;
