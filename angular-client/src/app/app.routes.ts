import { Routes } from '@angular/router';
import {AddGuestComponent} from './add-guest/add-guest.component';
import {GuestListComponent} from './guest-list/guest-list.component';
import {AppComponent} from './app.component';

export const routes: Routes = [
  {path: '', component: AppComponent},
  {path: 'guest-list', component: GuestListComponent},
  {path: 'add-guest', component: AddGuestComponent},
];

