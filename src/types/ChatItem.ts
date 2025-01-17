import { UserMessageData } from '../services/UserMessageService';
import { BotMessageData } from '../services/BotMessageService';

export interface ChatItem {
  id: string;
  userMessageData: UserMessageData;
  botMessageData: BotMessageData;
}
