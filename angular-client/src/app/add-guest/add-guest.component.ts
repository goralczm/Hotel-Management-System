import {Component, inject} from '@angular/core';
import {FormsModule} from '@angular/forms';
import {ApiService} from '../api.service';
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
  providers: [ ApiService ],
})
export class AddGuestComponent {
  apiService: ApiService;

  constructor(apiService: ApiService) {
    this.apiService = apiService;
  }

  onSubmit(data: any) {
    this.apiService
      .addGuest(data.value, [])
      .subscribe((guest: Guest) => {

      });
  }
}
