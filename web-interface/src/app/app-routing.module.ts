import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { WriterSelectorComponent } from './writer-selector/writer-selector.component';
import { WriterComponent } from './writer/writer.component';
import { WritingComponent } from './writing/writing.component';

const APP_ROUTES: Routes = [
  {
    path: '',
    component: WriterSelectorComponent,
    pathMatch: 'full'
  },
  {
    path: 'writer/:writerId',
    children: [
      {
        path: '',
        component: WriterComponent,
        pathMatch: 'full'
      },
      {
        path: 'writing/:writingId',
        component: WritingComponent
      }
    ]
  }
];

@NgModule({
  imports: [
    RouterModule.forRoot(APP_ROUTES)
  ],
  declarations: []
})
export class AppRoutingModule { }
