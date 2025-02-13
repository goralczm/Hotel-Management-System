import {Component, OnInit} from '@angular/core';
import {CommonModule} from '@angular/common';
import {HttpClientModule} from '@angular/common/http';
import {Guest} from '../../guest.interface';
import {GuestService} from '../guest.service';
import {FormBuilder, FormControl, FormGroup, FormsModule, ReactiveFormsModule} from '@angular/forms';
import {ToastComponent} from '../toast/toast.component';
import {NgbPagination} from '@ng-bootstrap/ng-bootstrap';
import {last} from 'rxjs';
import {AccessibilityOptionService} from '../accessibility-option.service';
import {AccessibilityOption} from '../../accessibility_option.interface';

@Component({
  selector: 'app-guest-list',
  imports: [
    CommonModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,
    ToastComponent,
    NgbPagination,
  ],
  templateUrl: './guest-list.component.html',
  styleUrl: './guest-list.component.css',
  providers: [
    GuestService,
    AccessibilityOptionService,
  ],
})
export class GuestListComponent implements OnInit {
  lastInteractedGuestId: number = -1;
  modalType: string = 'Register';
  myForm: FormGroup;
  lastSortingCondition: string = 'sort-id-asc';
  filterCondition: string = '';

  allGuests: Guest[] = [];
  allAccessibilityOptions: AccessibilityOption[] = [];
  filteredGuests: Guest[] = [];
  displayedGuests: Guest[] = [];
  guestDisplayLimit = 5;

  lastPage: number = 1;

  constructor(
    private guestService: GuestService,
    private accessibilityOptionService: AccessibilityOptionService,
    private formBuilder: FormBuilder,
  ) {
    this.setAccessibilityOptions();

    this.myForm = this.formBuilder.group({
      first_name: [''],
      last_name: [''],
      email: [''],
      address: [''],
      city: [''],
      country: [''],
      zip_code: [''],
      phone_number: [''],
      ...this.allAccessibilityOptions.reduce<Record<number, FormControl>>((acc, id) => {
        acc[id.id] = new FormControl(false);
        return acc;
      }, {})
    });
  }

  ngOnInit(): void {
    this.guestService
      .getAllGuests()
      .subscribe((guests) => {
        this.allGuests = guests;
        this.setPage(1);
        this.onGuestUpdated();
      });
  }

  searchOnChange(eventTarget: EventTarget | null): void {
    const target = eventTarget as HTMLInputElement;
    this.filterCondition = target.value;
    this.onGuestUpdated();
  }

  updateSortingCondition(eventTarget: EventTarget | null): void {
    const target = eventTarget as HTMLInputElement;
    this.lastSortingCondition = target.value;
    this.onGuestUpdated();
  }

  sortGuests() {
    this.allGuests.sort((a, b) => {
      switch (this.lastSortingCondition) {
        case 'sort-id-asc':
          if (a.id > b.id) return 1;
          else return -1;
        case 'sort-id-desc':
          if (a.id > b.id) return -1;
          else return 1;
        case 'sort-first-name-asc':
          return a.first_name.localeCompare(b.first_name)
        case 'sort-first-name-desc':
          return b.first_name.localeCompare(a.first_name)
        case 'sort-last-name-asc':
          return a.last_name.localeCompare(b.last_name)
        case 'sort-last-name-desc':
          return b.last_name.localeCompare(b.last_name)
      }

      return 0;
    });
  }

  filterGuests() {
    if (this.filterCondition === '') {
      this.filteredGuests = this.allGuests;
      return;
    }

    const searches: string[] = this.filterCondition.toLowerCase().split(' ');

    this.filteredGuests = [];

    const search = searches[0].toLowerCase();

    this.filteredGuests = this.allGuests.filter(guest =>
      guest.first_name.toLowerCase().includes(search) ||
      guest.last_name.toLowerCase().includes(search)
    )

    if (searches.length > 1) {
      for (let i = 1; i < searches.length; i++) {
        const search = searches[i].toLowerCase();
        if (search === '')
          continue;

        this.filteredGuests = this.filteredGuests.filter(guest =>
          guest.first_name.toLowerCase().includes(search) ||
          guest.last_name.toLowerCase().includes(search)
        );
      }
    }
  }

  onGuestUpdated(): void {
    this.sortGuests();
    this.filterGuests();
    this.refreshPage();
  }

  getPagesCount(): number {
    return Math.ceil(this.filteredGuests.length / this.guestDisplayLimit);
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
    if (this.filteredGuests.length === 0) {
      this.displayedGuests = [];
      return;
    }

    const leftIndex = (page - 1) * this.guestDisplayLimit;
    const rightIndex = leftIndex + this.guestDisplayLimit;

    this.displayedGuests = this.filteredGuests.slice(leftIndex, rightIndex);
  }

  refreshPage(): void {
    this.setPage(this.lastPage);
  }

  public disableFormInputs() {
    this.myForm.disable();

    this.myForm.patchValue({
      ...this.allAccessibilityOptions.reduce<Record<number, boolean>>((acc, id) => {
        acc[id.id] = false;
        return acc;
      }, {})
    });
  }

  public enableFormInputs() {
    this.myForm.enable();
  }

  public fillFormWithGuest() {
    this.guestService
      .getById(this.lastInteractedGuestId)
      .subscribe((guest: Guest) => {
        if (this.myForm)
        {
          const guestAccessibilityOptionIds = guest.accessibility_options.map(acc => acc.id);

          this.myForm.patchValue({...guest});
          this.myForm.patchValue({
            ...this.allAccessibilityOptions.reduce<Record<number, boolean>>((acc, id) => {
                acc[id.id] = guestAccessibilityOptionIds.includes(id.id);
              return acc;
            }, {})
          })
        }
      })
  }

  public guestModalButton() {
    switch (this.modalType) {
      case 'Register':
        this.createGuestSubmit();
        break;
      case 'Edit':
        this.putGuestSubmit();
        break;
      case 'View':
        this.modalType = 'Edit';
        this.enableFormInputs();
        break;
    }
  }

  public setAccessibilityOptions(): void {
    this.accessibilityOptionService
      .getAllAccessibilityOptions()
      .subscribe((accessibilityOptions) => {
        this.allAccessibilityOptions = accessibilityOptions;
      })
  }

  public createGuestSubmit() {
    let accessibilityOptions: number[] = [];
    for (const accessibilityOptionId of this.allAccessibilityOptions) {
      if (this.myForm.value[accessibilityOptionId.id.toString()] == true)
        accessibilityOptions.push(accessibilityOptionId.id);
    }

    this.guestService
      .addGuest(this.myForm.value, accessibilityOptions)
      .subscribe((guest: Guest) => {
        this.allGuests.push(guest);
        this.onGuestUpdated();
        ToastComponent.showToast("Create Guest", `User ${guest.first_name} ${guest.last_name} has been  added successfully.`);
      });
  }

  public putGuestSubmit() {
    let accessibilityOptions: number[] = [];
    for (const accessibilityOptionId of this.allAccessibilityOptions) {
      if (this.myForm.value[accessibilityOptionId.id.toString()] == true)
        accessibilityOptions.push(accessibilityOptionId.id);
    }

    console.log(accessibilityOptions);

    this.guestService
      .putGuest(this.lastInteractedGuestId, this.myForm.value, accessibilityOptions)
      .subscribe((guest: Guest) => {
        const index = this.allGuests.findIndex(g => g.id === this.lastInteractedGuestId);
        this.allGuests[index] = guest;
        this.onGuestUpdated();
        ToastComponent.showToast("Edit Guest", `User ${guest.first_name} ${guest.last_name} has been edited successfully.`);
      })
  }

  public deleteUser(guestId: number): void {
    this.guestService
      .deleteGuest(guestId)
      .subscribe((response: any) => {
        const guest = this.allGuests.find(g => guestId === g.id);
        this.allGuests = this.allGuests.filter(guest => guestId !== guest.id);
        this.onGuestUpdated();
        ToastComponent.showToast("Delete Guest", `User ${guest?.first_name} ${guest?.last_name} has been deleted successfully.`);
      });
  }
}
