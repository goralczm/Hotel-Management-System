import {Component, inject, OnInit} from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {Guest} from '../../guest.interface';
import {ApiService} from '../api.service';
import {HttpClientModule} from '@angular/common/http';

@Component({
  selector: 'app-guest-view',
  imports: [
    HttpClientModule,
  ],
  templateUrl: './guest-view.component.html',
  styleUrl: './guest-view.component.css',
  providers: [ ApiService ]
})
export class GuestViewComponent implements OnInit {
  private readonly route = inject(ActivatedRoute);
  guest: Guest | undefined;

  constructor(private apiService: ApiService) {}

  ngOnInit() {
    const idParam = Number(this.route.snapshot.paramMap.get('id'));
    if (isNaN(idParam))
      window.location.href = 'guest-list';

    this.apiService.getById(idParam).subscribe(guest => {
      this.guest = guest;
    });
  }
}
