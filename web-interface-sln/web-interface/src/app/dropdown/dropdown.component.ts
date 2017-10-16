import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-dropdown',
  templateUrl: './dropdown.component.html',
  styleUrls: ['./dropdown.component.css']
})
export class DropdownComponent implements OnInit {
  @Input() tooltip: string;
  show = false;

  constructor() { }

  ngOnInit() {
  }

  toggle() {
    this.show = !this.show;
  }

}
