import { Component, OnInit } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';
import { Observable } from 'rxjs/Observable';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  small$: Observable<boolean>;
  constructor(private router: Router) { }
  ngOnInit(): void {
    this.small$ = this.router.events.filter(x => x instanceof NavigationEnd)
      .map(x => (x as NavigationEnd).url !== '/');
  }

}
