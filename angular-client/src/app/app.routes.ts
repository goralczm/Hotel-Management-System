import { Routes } from '@angular/router';
import {AddGuestComponent} from './add-guest/add-guest.component';
import {GuestListComponent} from './guest-list/guest-list.component';
import {AppComponent} from './app.component';
import {GuestViewComponent} from './guest-view/guest-view.component';

export const routes: Routes = [
  {path: '', redirectTo: '/guest-list', pathMatch: 'full'},
  {path: 'guest-list', component: GuestListComponent},
  {path: 'guest/:id', component: GuestViewComponent},
];

