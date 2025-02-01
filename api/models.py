from sqlmodel import SQLModel, Field, Relationship
from pydantic import field_validator
from datetime import datetime
from typing import Dict, List, Optional

#Base on Current user examples
class Quiz(SQLModel):
  id: Optional[int] = Field(primary_key=True)  # Example: 43
  name: Optional[str] = Field(default=None)
  title: Optional[str] = None  # Example: "Structural Organisation in Animals and Plants (7)"
  description: str = Field(default="")
  difficulty_level: Optional[int]
  topic: str  # Example: "Structural Organisation in Animals"
  time: datetime  # Example: "2024-07-03T00:00:00.000+05:30"
  is_published: bool

  # BeCare with date time 
  created_at: datetime  # Example: "2024-07-03T11:00:08.958+05:30"
  updated_at: datetime  # Example: "2024-09-23T18:43:27.751+05:30"
  duration: int  # Example: 128 (duration and question_counts are same, this means that each question have 1 minute)
  end_time: datetime  # Example: "2024-07-04T00:00:00.000+05:30"
  
  negative_marks: Optional[float] = Field(default=None)  # Example: 1.0
  correct_answer_marks: Optional[float] = Field(default=None)  # Example: 4.0
  shuffle: bool
  show_answers: bool
  lock_solutions: bool
  is_form: bool
  show_mastery_option: bool
  quiz_type: Optional[str] = None
  is_custom: bool
  banner_id: Optional[str] = None  # Pointing to banner table id
  exam_id: Optional[str] = None  # Pointing to exam table id
  show_unanswered: bool
  ends_at: datetime  # Example: "2025-01-18"
  lives: Optional[str] = None
  live_count: str  # Example: "Free Test"
  coin_count: Optional[int] = Field(default=None)  # Example: -1
  questions_count: int  # Example: 128 (duration and questions_counts are same, this means that each question have 1 minute)
  daily_date: Optional[str]  # Example: "January 17, 2025"
  max_mistake_count: int  # Example: 15
  questions: List["Question"] = Relationship(back_populates="quiz", link_model="question")

class Question(SQLModel):
  id: int | None = Field(primary_key=True)  # Example: 1827
  description: str  # Example: "The tissue which has free surface that faces either a body fluid or the outside environment is called characteristics of the"
  difficulty_level: str | int = None
  topic: str  # Example: "structural organisation in animals"
  is_published: bool
  
  created_at: datetime  # Example: "2024-07-02T12:43:34.360+05:30" (creation and updating date are not same)
  updated_at: datetime  # Example: "2024-11-30T18:39:20.587+05:30" (creation and updating date are not same)
  
  detailed_solution: str  # Example: "**Explanation:**\n\nThe tissue that has a free surface is called **epithelial tissue**. This free surface may face either a body fluid (such as blood, lymph, or mucus) or the outside environment.\n\n**Characteristics of Epithelial Tissue:**\n\n* **Free Surface:** The cells have an exposed surface that faces either a body fluid or the external environment.\n* **Apical Surface:** The surface facing the external environment or body cavity.\n* **Basal Surface:** The surface attached to the connective tissue below.\n* **Closely Packed:** The cells are closely packed together with minimal intercellular space.\n* **Polarized Cells:** They are generally polarized, with different apical and basal surfaces and functions.\n* **Basement Membrane:** The basal surface is supported by a basement membrane, which separates the epithelium from the underlying connective tissue.\n* **Avascular:** Epithelial cells are avascular, meaning they lack blood vessels. They receive nutrients from the underlying connective tissue through diffusion.\n\n**Functions of Epithelial Tissue:**\n\n* **Protection:** Forms a physical barrier against pathogens, chemicals, and physical damage.\n* **Secretion:** Secretes various substances, such as mucus, enzymes, and hormones.\n* **Absorption:** Facilitates the uptake of substances from the external environment or body fluids.\n* **Excretion:** Helps eliminate waste products from the body.\n* **Sensory:** Contains specialized cells that detect changes in the environment and transmit sensory information.\n\n**Additional Context:**\n\nEpithelial tissue is classified into different types based on its structure and function. Some of the common types include:\n\n* **Simple Epithelium:** Consists of a single layer of cells.\n* **Stratified Epithelium:** Consists of multiple layers of cells.\n* **Glandular Epithelium:** Specialized for secretion of substances.\n* **Sensory Epithelium:** Contains specialized sensory cells."
  type: str = None
  is_mandatory: bool
  show_in_feed: bool
  pyq_label: str | int = None
  topic_id: int  # Pointing to topic table id
  reading_material_id: int  # Pointing to reading material table id
  fixed_at: str = None
  fix_summary: str = None
  created_by: str = None
  updated_by: str = None
  quiz_label: str = None
  question_from: str  # Example: "Q-bank"
  language: str = None
  photo_url: str = None
  photo_solution_url: str = None
  is_saved: bool
  tag: str = Field(default="")
  options: List["Option"] = Relationship(back_populates="question", link_model="option")

class Option(SQLModel):
  id: int | None = Field(primary_key=True)  # Example: 7321
  description: str = Field(default=None)  # Example: "Muscular tissue"
  question_id: int = Field(foreign_key="question.id")  # Example: 1827
  is_correct: bool
  created_at: datetime  # Example: "2024-07-02T12:43:34.365+05:30" (creation and updating date all are same)
  updated_at: datetime  # Example: "2024-07-02T12:43:34.365+05:30" (creation and updating date all are same)
  unanswered: bool
  photo_url: str

class SubmissionData(SQLModel):  
    id: int | None = Field(default=None, primary_key=True)
    quiz_id: int = Field(foreign_key="quiz.id")
    user_id: str  
    submitted_at: datetime  
    created_at: datetime  
    updated_at: datetime  
    score: int  
    trophy_level: int  
    accuracy: float  # Store accuracy as a float (0-1)
    speed: int  
    final_score: float  
    negative_score: float  
    correct_answers: int  
    incorrect_answers: int  
    source: str  
    type: str  
    started_at: datetime  
    ended_at: datetime  
    duration: str  
    better_than: int  
    total_questions: int  
    rank_text: str  
    mistakes_corrected: int  
    initial_mistake_count: int  
    response_map: Dict[str, int]  
    quiz: "Quiz"
    reading_materials: List[str] = Field(default=[])  
    next_steps: List["NextStep"] = Relationship(back_populates="submission_data", link_model="NextStep")

    @field_validator("accuracy", mode="before")
    @classmethod
    def parse_accuracy(cls, value: str) -> float:
        """Convert accuracy from percentage string to float (0-1)."""
        if isinstance(value, str) and "%" in value:
            return float(value.replace("%", "").strip()) / 100
        return float(value)

class NextStep(SQLModel):
    pageType: str  

# a simple college dataset with NEET rank ranges
colleges = {
    "College A": {"rank_lower": 1, "rank_upper": 1000},
    "College B": {"rank_lower": 1001, "rank_upper": 5000},
    "College C": {"rank_lower": 5001, "rank_upper": 10000},
    "College D": {"rank_lower": 10001, "rank_upper": 20000},
    "College E": {"rank_lower": 20001, "rank_upper": 50000},
    "College F": {"rank_lower": 50001, "rank_upper": 100000}
}