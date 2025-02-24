import { BotMessageData } from '@services/BotMessageService';


export interface ChatItem {
  userMessage: string;
  botMessageData: BotMessageData;
}
