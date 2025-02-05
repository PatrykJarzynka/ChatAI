import { ChatItem } from '../types/ChatItem';
import { ChatResponse } from '../models/ChatResponse';


export interface Chat extends Omit<ChatResponse, 'chatItems'> {
  chatItems: ChatItem[];
}
