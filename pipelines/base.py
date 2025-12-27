from abc import ABC, abstractmethod



class BasicBaseline(ABC):
    """
    
    Abstract base class for all QA pipelines.

    """

    @abstractmethod
    def answer(self, question, claim = ""):
        """
    
        Generating answer for a question 

        """

        pass
    