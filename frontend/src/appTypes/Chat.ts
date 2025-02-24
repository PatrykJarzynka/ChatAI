import { ChatItem } from 'appTypes/ChatItem';
import { ChatResponse } from '@models/ChatResponse';


export interface Chat extends Omit<ChatResponse, 'chatItems'> {
  chatItems: ChatItem[];
}
