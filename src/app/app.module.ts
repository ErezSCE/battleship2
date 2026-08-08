import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { RouterModule } from '@angular/router';
import { AppComponent } from './app.component';
import { AppRoutingModule } from './app-routing.module';
import { BoardComponent } from './board/board.component';
import { OpponentBoardComponent } from './board/opponent-board.component';

@NgModule({
  declarations: [AppComponent, BoardComponent, OpponentBoardComponent],
  imports: [BrowserModule, RouterModule, AppRoutingModule],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {}
