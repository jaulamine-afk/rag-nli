# scripts/run_experiments.py

import pickle

from datasets import load_dataset
from rag.generator import Generator

from rag.retriever import BasicRetriever
from nli.nli_class import NLIModel

from pipelines.rag_baseline import RAGBaseline
from pipelines.rag_nli import RAG_NLI
from pipelines.rag_nli_subclaim import RAG_NLI_Subclaim

from evaluation.evaluate import evaluate_pipeline, run_experiment




#claim used for NLI

claims = [
    "Scott Derrickson and Ed Wood share the same nationality.",
    "There exists a government position held by the actress who played Corliss Archer in Kiss and Tell.",
    "There exists a science fantasy young adult series told in first person with companion books about enslaved worlds and alien species.",
    "The Laleli Mosque and Esma Sultan Mansion are located in the same neighborhood.",
    "There exists a New York city where the director of Big Stone Gap is based.",
    "There exists a person who formed the South Korean boy group that released the debut album 2014 S/S.",
    "There exists a person known by the stage name Aladin who worked as a consultant helping organizations.",
    "There exists a capacity number for the arena where the Lewiston Maineiacs played home games.",
    "One of Annie Morton or Terry Richardson is older than the other.",
    "Local H and For Against are both from the United States.",
    "There exists a fight song for the university with its main campus in Lawrence, Kansas.",
    "There exists a screenwriter credited for Evolution who co-wrote a film with Nicolas Cage and Téa Leoni.",
    "There exists a year when Guns N Roses performed a promo for an Arnold Schwarzenegger film.",
    "Random House Tower and 888 7th Avenue are both used for real estate.",
    "There exists a timeframe when the manager who recruited David Beckham managed Manchester United.",
    "There exists a population count for the country where Brown State Fishing Lake is located.",
    "There exists a former name for the conference where Vermont Catamounts soccer competes.",
    "Giuseppe Verdi and Ambroise Thomas are both opera composers.",
    "There exists a presidential administration during which Roger O. Egeberg served as Assistant Secretary.",
    "One of Henry Roth or Robert Erskine Childers was from England.",
    "There exists a Mexican Formula One driver who held the podium besides the Force India driver.",
    "There exists a hedgehog voiced by the singer of A Rather Blustery Day.",
    "There exists a device that can control the same program as the Apple Remote.",
    "One of Badly Drawn Boy or Wolf Alice has a higher instrument to person ratio.",
    "There exists a distinction that Kasper Schmeichel's father was voted for by IFFHS in 1992.",
    "There exists a writer of These Boots Are Made for Walkin' who died in 2007.",
    "There exists a founding year for Virginia Commonwealth University.",
    "Dictyosperma and Huernia are both described as a genus.",
    "There exists an American industrialist who founded Kaiser Ventures and is known for shipbuilding.",
    "There exists a name for adventures in the game Tunnels and Trolls.",
    "There exists a release date for Poison's album Shut Up, Make Love.",
    "There exists a place where Buck-Tick originates from.",
    "There exists a French ace pilot and adventurer who flew L'Oiseau Blanc.",
    "Freakonomics and In the Realm of the Hackers are both American documentaries.",
    "One of Letters to Cleo or Screaming Trees had more members.",
    "There exists an end date for the civil war in which Alexander Kerensky was defeated.",
    "There exists a year since which the author of Seven Brief Lessons on Physics has worked in France.",
    "There exists a war with over 60 million casualties commemorated by Livesey Hal War Memorial.",
    "Elko Regional Airport and Gerald R. Ford International Airport are both located in Michigan.",
    "There exists a city where Ralph Hefferline's university is located.",
    "One of Manchester Terrier or Scotch Collie has ancestors including Gordon and Irish Setters.",
    "There exists a headquarters location for the company where Sachin Warrier worked.",
    "There exists a birth year for the creator of the manga about Ichitaka Seto.",
    "There exists something secured for Ethiopia in the battle where Giuseppe Arimondi died.",
    "There exists a US Vice President under whom Alfred Balk served in a committee role.",
    "There exists a coastal area bordering the medieval fortress in Dirleton.",
    "There exists a writer of a song inspired by a tombstone that appeared on Back to Mono.",
    "There exists a type of forum initiated by a former Soviet statesman.",
    "Ferocactus and Silene are both types of plant.",
    "There exists a British jet-powered medium bomber used in the South West Pacific during WWII.",
    "There exists a year and conference for Colorado Buffaloes' 14th season with a 2-6 record.",
    "There exists a number of hypermarkets operated by the chain that bought Euromarché.",
    "There exists a midwest race track hosting a 500 mile race every May.",
    "There exists a city where the Prince of Tenors starred in a Puccini opera film.",
    "There exists other writers who worked with Ellie Goulding on Delirium.",
    "There exists an Australian city founded in 1838 with a school opened by a Prime Minister.",
    "There exists an oversteering technique that D1NZ is based on.",
    "One of Keith Bostic or Jerry Glanville is younger.",
    "There exists a population for the city where Kirton End is located according to 2001 census.",
    "Cypress and Ajuga are both genera.",
    "There exists a distinction held by a former NBA player who coached Charlotte Sting.",
    "There exists an executive producer for a film scored by Jerry Goldsmith.",
    "One of Emma Bull or Virginia Woolf was born earlier.",
    "There exists a Roud Folk Song Index for the nursery rhyme inspiring What Are Little Girls Made Of.",
    "There exists a number of countries where a corporation criticized by Scott Parkin operates.",
    "There exists a WB supernatural drama series that Rose Mcgowan was known for.",
    "There exists a Hall of Fame recognizing the organization where Vince Phillips held a title.",
    "There exists a singer whose song was the lead single from Confessions.",
    "There exists a younger brother of guest stars from The Hard Easy.",
    "There exists a sponsored league cup that Wigan Athletic competes in.",
    "There exists an American animated series voiced by Tara Strong based on Teen Titans.",
    "There exists an inhabitant name for the city where 122nd SS-Standarte was formed.",
    "There exists a color of clothing worn during Koningsdag in the Netherlands.",
    "There exists a 1996 Romeo & Juliet adaptation written by James Gunn.",
    "There exists a former Governor of Arkansas under whom Robert Suettinger served.",
    "There exists an American Hawaiian surfer born in 1992 who won Rip Curl Pro Portugal.",
    "There exists a middle name for the actress who plays Bobbi Bacha.",
    "There exists a tribe of indigenous people with whom Alvaro Mexia had a diplomatic mission.",
    "Alfred Gell and Edmund Leach share the same nationality.",
    "There exists a birth year for the King who made the 1925 Birthday Honours.",
    "There exists a county seat for the county containing East Lempster, New Hampshire.",
    "There exists a stage name for the rock singer who released Against the Wind.",
    "There exists a way of filling armed forces vacancies that was deemed constitutional.",
    "There exists an American confectionery company based in Illinois that sells Handi-Snacks.",
    "There exists a woman from a book about Clinton who was a former white house intern.",
    "There exists a birth date for an American lawyer in Trump's presidential campaign.",
    "There exists a publication year for the novel that inspired Nina by Lourenço Mutarelli.",
    "Teide National Park and Garajonay National Park are located in the same place.",
    "There exists a sales number for Roald Dahl's variation on an anecdote.",
    "Chris Menges and Aram Avakian share the same occupation.",
    "There exists a not-for-profit media outlet co-founded by Andrew Jaspan.",
    "There exists an American film director who hosted the 18th Independent Spirit Awards.",
    "There exists a location of a hotel and casino where Bill Cosby recorded an album.",
    "Gibson and Zurracapote are both drinks that contain gin.",
    "There exists a month for an annual documentary film festival presented by a British journal.",
    "There exists a county where Tysons Galleria is located.",
    "There exists a type of product provided by the company where Bordan Tkachuk was CEO.",
    "One of Lev Yilmaz or Pamela B. Green was known for animation.",
    "There exists a city where the ambassador of Rabat-Salé-Kénitra to China is based.",
    "Yingkou and Fuding are the same level of city.",
]

# Load dataset from pickle

with open('data/hotpotqa_300.pkl', 'rb') as f:
    ds_100 = pickle.load(f)


basic_retriever = BasicRetriever(ds_100)
nli_model = NLIModel()
generator = Generator(model_name = "google/flan-t5-small")


# Load three pipelines to compare

rag_pipeline = RAGBaseline(basic_retriever, generator)

rag_nli_pipeline = RAG_NLI(basic_retriever, generator, nli_model) 

rag_nli_sub_pipeline = RAG_NLI_Subclaim(basic_retriever, generator, nli_model)



print(run_experiment(ds_100,claims,rag_pipeline, rag_nli_pipeline, rag_nli_sub_pipeline))