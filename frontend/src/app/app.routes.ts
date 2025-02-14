import { Routes } from '@angular/router';
import { AuthView } from './components/views/auth-view/auth-view.component';
import { ChatView } from './components/views/chat-view/chat-view.component';


export const routes: Routes = [
  { path: '', component: AuthView },
  { path: 'chat', component: ChatView }
];
