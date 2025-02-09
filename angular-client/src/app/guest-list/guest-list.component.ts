import {Component, OnInit} from '@angular/core';
import {CommonModule} from '@angular/common';
import {HttpClientModule} from '@angular/common/http';
import {Guest} from '../../guest.interface';
import {ApiService} from '../api.service';
import {FormBuilder, FormGroup, FormsModule, ReactiveFormsModule} from '@angular/forms';
import {ToastComponent} from '../toast/toast.component';

@Component({
  selector: 'app-guest-list',
  imports: [
    CommonModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,
    ToastComponent,
  ],
  templateUrl: './guest-list.component.html',
  styleUrl: './guest-list.component.css',
  providers: [ ApiService ],
})
export class GuestListComponent implements OnInit {
  apiService: ApiService;
  lastInteractedGuestId: number = -1;
  modalType: string = 'Register';
  myForm: FormGroup;
  lastPage: number = 1;
  lastSortingCondition: string = 'sort-id-asc';
  filterCondition: string = '';

  allGuests: Guest[] = [];
  filteredGuests: Guest[] = [];
  displayedGuests: Guest[] = [];
  guestDisplayLimit = 5;

  constructor(apiService: ApiService, private formBuilder: FormBuilder) {
    this.apiService = apiService;

    this.myForm = this.formBuilder.group({
      first_name: [''],
      last_name: [''],
      email: [''],
      address: [''],
      city: [''],
      country: [''],
      zip_code: [''],
      phone_number: [''],
    });
  }

  ngOnInit(): void {
    this.apiService
      .getAllGuests()
      .subscribe((guests) => {
        this.allGuests = guests;
        this.setPage(1);
        this.updateGuests();
      });
  }

  searchOnChange(eventTarget: EventTarget | null): void {
    const target = eventTarget as HTMLSelectElement;
    this.filterCondition = target.value;
    this.updateGuests()
  }

  updateSortingCondition(eventTarget: EventTarget | null): void {
    const target = eventTarget as HTMLSelectElement;
    this.lastSortingCondition = target.value;
    this.updateGuests();
  }

  sortGuests() {
    this.allGuests.sort((a, b) => {
      switch (this.lastSortingCondition)
      {
        case 'sort-id-asc':
          if (a.id > b.id)
            return 1;
          else
            return -1;
        case 'sort-id-desc':
          if (a.id > b.id)
            return -1;
          else
            return 1;
        case 'sort-first-name-asc':
          if (a.first_name > b.first_name)
            return 1;
          else
            return -1;
        case 'sort-first-name-desc':
          if (a.first_name > b.first_name)
            return -1;
          else
            return 1;
        case 'sort-last-name-asc':
          if (a.last_name > b.last_name)
            return 1;
          else
            return -1;
        case 'sort-last-name-desc':
          if (a.last_name > b.last_name)
            return -1;
          else
            return 1;
      }

      return 0;
    });
  }

  filterGuests() {
    this.filteredGuests = this.allGuests.filter(guest => guest.first_name.includes(this.filterCondition) || guest.last_name.includes(this.filterCondition));
  }

  updateGuests(): void {
    this.sortGuests();
    this.filterGuests();
    this.refreshPage();
  }

  getPagesCount(): number {
    return Math.ceil(this.allGuests.length / this.guestDisplayLimit);
  }

  displayLimitSelectChanged(eventTarget: EventTarget | null): void {
    const target = eventTarget as HTMLSelectElement;

    this.setDisplayLimit(Number(target.value));
  }

  setDisplayLimit(limit: number) {
    this.guestDisplayLimit = limit;
    this.refreshPage()
  }

  setPage(page: number): void {
    if (this.allGuests.length === 0)
    {
      this.displayedGuests = [];
      return;
    }

    if (page <= 0)
    {
      this.setPage(1);
      return;
    }

    if (page > this.getPagesCount())
    {
      this.setPage(this.getPagesCount());
      return;
    }

    const leftIndex = (page - 1) * this.guestDisplayLimit;
    const rightIndex = leftIndex + this.guestDisplayLimit;

    this.displayedGuests = this.filteredGuests.slice(leftIndex, rightIndex);
    this.lastPage = page;
  }

  refreshPage(): void {
    this.setPage(this.lastPage);
  }

  public createGuestSubmit(data: any) {
    this.apiService
      .addGuest(data.value, [])
      .subscribe((guest: Guest) => {
        this.allGuests.push(guest);
        this.updateGuests();
        ToastComponent.showToast("Create Guest", `User ${guest.first_name} ${guest.last_name} has been  added successfully.`);
      });
  }

  public putGuestSubmit(data: any) {
    this.apiService
      .putGuest(this.lastInteractedGuestId, data.value)
      .subscribe((guest: Guest) => {
        const index = this.allGuests.findIndex(g => g.id === this.lastInteractedGuestId);
        this.allGuests[index] = guest;
        this.updateGuests();
        ToastComponent.showToast("Edit Guest", `User ${guest.first_name} ${guest.last_name} has been edited successfully.`);
      })
  }

  public fillFormWithGuest(data: any) {
    console.log(data);
    this.apiService
      .getById(this.lastInteractedGuestId)
      .subscribe((guest: Guest) => {
        if (this.myForm)
          this.myForm.patchValue({ ...guest });
      })
  }

  public deleteUser(guestId: number): void {
    this.apiService
      .deleteGuest(guestId)
      .subscribe((response: any) => {
        const guest = this.allGuests.find(g => guestId === g.id);
        this.allGuests = this.allGuests.filter(guest => guestId !== guest.id);
        this.updateGuests();
        ToastComponent.showToast("Delete Guest", `User ${guest?.first_name} ${guest?.last_name} has been deleted successfully.`);
      });
  }
}
