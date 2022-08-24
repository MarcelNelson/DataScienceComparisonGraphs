#Data Science Industry Comparison Charts
#Created a simple website to visualize graphs made with Global Data Science Salary data from Kaggle
#Purpose of the project is to show Data Scientists the average salaries in their field based on experience level, company size, job title and other metrics.
#Utilizes Okteto's services to host and maintain a live 24/7 website.
#Employs Postgresql and DBeaver to store and manage data from Kaggle.com
#Graphs visualized and formatted using Jinja2, Plotly, and CSS.









from fastapi import FastAPI, Depends, Request
from sqlalchemy.orm import Session

from . import crud, models
from .database import SessionLocal, engine

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import plotly.express as px
import pandas as pd

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def welcome(request: Request, db: Session=Depends(get_db)):
  x = crud.get_datascience(db)
  df = pd.DataFrame.from_records(x,columns=['Work_year', 'Experience_level', 'Employment_type', 'Job_title', 'Salary', 'Salary_currency', 'Salary_usd', 'Employee_residence', 'Remote_work_percent', 'Company_Location', 'Company_size'])

  px.defaults.width = 266
  px.defaults.height = 200

  figexp= df.groupby('Experience_level')['Salary_usd'].mean()
  figexp=figexp.reset_index()
  figexp=figexp.sort_values('Salary_usd',ascending=False).head(10)
  figexp=df.loc[df['Experience_level'].isin(figexp.Experience_level)]

  fig_experience = px.bar(figexp,x='Experience_level', y='Salary_usd', color='Job_title').update_xaxes(categoryorder="total descending")
  fig_experience.update_layout(yaxis=dict(tickfont=dict(size=5)),
  xaxis = dict(tickfont = dict(size=5)),
  font=dict(size=5),
  margin=dict(l=0, r=0, t=0, b=0))
  exp10=fig_experience.to_html(full_html=False, include_plotlyjs='cdn')

  figloc= df.groupby('Job_title')['Salary_usd'].mean()
  figloc=figloc.reset_index()
  figloc=figloc.sort_values('Salary_usd',ascending=False).head(10)
  figloc=df.loc[df['Job_title'].isin(figloc.Job_title)]

  fig_location = px.bar(figloc,x='Job_title', y='Salary_usd', color='Company_Location').update_xaxes(categoryorder="total descending")
  fig_location.update_layout(yaxis=dict(tickfont=dict(size=5)),
  xaxis = dict(tickfont = dict(size=5)),
  font=dict(size=5),
  margin=dict(l=0, r=0, t=0, b=0))
  location10=fig_location.to_html(full_html=False, include_plotlyjs='cdn')

  dfpie = df.groupby('Employment_type')['Remote_work_percent'].mean()
  dfpie=dfpie.reset_index()
  dfpie=dfpie.sort_values('Remote_work_percent', ascending=False)
  #dfpie=df.loc[df['Employment_type'].isin(dfpie.Employment_type)]

  figpie = px.pie(dfpie, values='Remote_work_percent', names='Employment_type')
  figpie.update_layout(yaxis=dict(tickfont=dict(size=5)),
  xaxis = dict(tickfont=dict(size=5)),
  font=dict(size=5),
  margin=dict(l=0, r=0, t=0, b=0))
  pospie = figpie.to_html(full_html=False, include_plotlyjs='cdn')

  dfbyyear = df.groupby('Work_year')['Salary_usd'].mean()
  dfbyyear = dfbyyear.reset_index()
  dfbyyear = dfbyyear.sort_values('Work_year', ascending=False)
  #dfbyyear = df.loc[df['Work_year'].isin(dfbyyear.Work_year)]

  dfyear = px.line(dfbyyear, x="Work_year", y="Salary_usd", color_discrete_sequence=['black'], markers = True).update_xaxes(categoryorder="total ascending")
  dfyear.update_layout(yaxis=dict(tickfont=dict(size=5)),
  xaxis = dict(tickfont=dict(size=5)),
  font=dict(size=5),
  margin=dict(l=0, r=0, t=0, b=0))
  figyear = dfyear.to_html(full_html=False, include_plotlyjs='cdn')

  #dfyearly = df.groupby(['Work_year','Job_title'])['Salary_usd'].mean()
  #dfyearly = dfyearly.reset_index()
  #dfyearly = dfyearly.sort_values(['Work_year', 'Job_title'], ascending=False).head(3)
  #dfyearly=df.loc[df['Job_title'].isin(figloc.Job_title)]

  dfbyyearly = df.groupby('Work_year')['Salary_usd'].mean()
  dfbyyearly = dfbyyearly.reset_index()
  dfbyyearly = dfbyyearly.sort_values('Work_year', ascending=False)
  dfbyyearly = df.loc[df['Work_year'].isin(dfbyyearly.Work_year)]

  top4 = dfbyyearly.groupby('Job_title')['Salary_usd'].mean().sort_values(ascending=False).head(4)
  top4 = top4.reset_index()

  yearly = px.line(dfbyyearly.loc[dfbyyearly['Job_title'].isin(top4.Job_title)], x="Work_year", y= "Job_title", markers = True).update_xaxes(categoryorder='total ascending')
  yearly.update_layout(yaxis=dict(tickfont=dict(size=5)),
  xaxis = dict(tickfont=dict(size=5)),
  font=dict(size=5),
  margin=dict(l=0, r=0, t=0, b=0))
  figly = yearly.to_html(full_html=False, include_plotlyjs='cdn')

  figsize= df.groupby('Company_size')['Salary_usd'].mean()
  figsize=figsize.reset_index()
  figsize=figsize.sort_values('Salary_usd',ascending=False).head(10)
  figsize=df.loc[df['Company_size'].isin(figsize.Company_size)]

  fig_size = px.bar(figsize,x='Company_size', y='Salary_usd', color='Job_title').update_xaxes(categoryorder="total descending")
  fig_size.update_layout(yaxis=dict(tickfont=dict(size=5)),
  xaxis = dict(tickfont = dict(size=5)),
  font=dict(size=5),
  margin=dict(l=0, r=0, t=0, b=0))
  size10=fig_size.to_html(full_html=False, include_plotlyjs='cdn')


  figtotal = px.histogram(df, x="Salary_usd")
  figtotal.update_layout(yaxis=dict(tickfont=dict(size=5)),
  xaxis = dict(tickfont = dict(size=5)),
  font=dict(size=5),
  margin=dict(l=0, r=0, t=0, b=0))
  total=fig_total.to_html(full_html=False, include_plotlyjs='cdn')



  #dfteam=df.groupby('Team')['Salary'].sum()
  #dfteam=dfteam.reset_index()
  #dfteam=dfteam.sort_values('Salary',ascending=False).head(10)
  #dfteam=df.loc[df['Team'].isin(dfteam.Team)]

  #figteam=px.bar(dfteam,x='Team',y='Salary', color='Position').update_xaxes(categoryorder="total descending")
  #figteam.update_layout(yaxis=dict(tickfont=dict(size=5)),
  #xaxis=dict(tickfont=dict(size=5)),
  #font=dict(size=5),
  #margin=dict(l=0, r=0, t=0, b=0))
  #teamsalary=figteam.to_html(full_html=False, include_plotlyjs='cdn')

  #pos10=dfteam.groupby('Position')['Salary'].mean().sort_values(ascending=False).head(10)
  #pos10=pos10.reset_index()
  #figpos=px.box(dfteam.loc[dfteam['Position'].isin(pos10.Position)], x='Position', y='Salary')
  #figpos.update_layout(yaxis=dict(tickfont=dict(size=5)),
  #xaxis=dict(tickfont=dict(size=5)),
  #font=dict(size=5),
  #margin=dict(l=0, r=0, t=0, b=0))
  #possalary=figpos.to_html(full_html=False, include_plotlyjs='cdn')

  #bottom10 = df.groupby('Team')['Salary'].sum()
  #bottom10 = bottom10.reset_index()
  #bottom10 = dfteam.sort_values('Salary', ascending=False).tail(10)
  #dfteam = df.loc[df['Team'].isin(bottom10.Team)]

  #pos10 = dfteam.groupby('Position')['Salary'].mean().sort_values(ascending=False).head(10)
  #pos10 = pos10.reset_index()
  #figpos2 = px.box(dfteam.loc[dfteam['Position'].isin(pos10.Position)], x='Position', y='Salary', color_discrete_sequence=['red'])
  #figpos2.update_layout(yaxis=dict(tickfont=dict(size=5)),
  #xaxis = dict(tickfont=dict(size=5)),
  #font=dict(size=5),
  #margin=dict(l=0, r=0, t=0, b=0))
  #possalary2 = figpos2.to_html(full_html=False, include_plotlyjs='cdn')

  #dfteam = df.groupby('Position')['Salary'].mean()
  #dfteam = dfteam.reset_index()
  #dfteam.sort_values('Salary', ascending=False)

  #figpie = px.pie(dfteam, values='Salary', names='Position')
  #figpie.update_layout(yaxis=dict(tickfont=dict(size=5)),
  #xaxis = dict(tickfont=dict(size=5)),
  #font=dict(size=5),
  #margin=dict(l=0, r=0, t=0, b=0))
  #pospie = figpie.to_html(full_html=False, include_plotlyjs='cdn')



  return templates.TemplateResponse("chart.html", {"request": request, "exp10": exp10, "location10": location10, "pospie": pospie, "figyear": figyear, "total": total, "size10": size10})
