import {Component, inject} from '@angular/core';
import {FormsModule} from '@angular/forms';
import {GuestService} from '../guest.service';
import {HttpClientModule} from '@angular/common/http';
import {Guest} from '../../guest.interface';

@Component({
  standalone: true,
  selector: 'app-add-guest',
  imports: [
    FormsModule,
    HttpClientModule,
  ],
  templateUrl: './add-guest.component.html',
  styleUrl: './add-guest.component.css',
  providers: [ GuestService ],
})
export class AddGuestComponent {
  apiService: GuestService;

  constructor(apiService: GuestService) {
    this.apiService = apiService;
  }

  onSubmit(data: any) {
    this.apiService
      .addGuest(data.value, [])
      .subscribe((guest: Guest) => {

      });
  }
}
