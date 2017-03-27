from __future__ import division
import re
import operator


class SummaryTool(object):
    def __init__(self):
        self.stopwords = set(
            ["able", "about", "above", "abroad", "according", "accordingly", "across", "actually", "adj", "after",
             "afterwards", "again", "against", "ago", "ahead", "ain't", "all", "allow", "allows", "almost", "alone",
             "along",
             "alongside", "already", "also", "although", "always", "am", "amid", "amidst", "among", "amongst", "an",
             "and",
             "another", "any", "anybody", "anyhow", "anyone", "anything", "anyway", "anyways", "anywhere", "apart",
             "appear",
             "appreciate", "appropriate", "are", "aren't", "around", "as", "a's", "aside", "ask", "asking",
             "associated",
             "at", "available", "away", "awfully", "back", "backward", "backwards", "be", "became", "because", "become",
             "becomes", "becoming", "been", "before", "beforehand", "begin", "behind", "being", "believe", "below",
             "beside",
             "besides", "best", "better", "between", "beyond", "both", "brief", "but", "by", "came", "can", "cannot",
             "cant",
             "can't", "caption", "cause", "causes", "certain", "certainly", "changes", "clearly", "c'mon", "co", "co.",
             "com",
             "come", "comes", "concerning", "consequently", "consider", "considering", "contain", "containing",
             "contains",
             "corresponding", "could", "couldn't", "course", "c's", "currently", "dare", "daren't", "definitely",
             "described",
             "despite", "did", "didn't", "different", "directly", "do", "does", "doesn't", "doing", "done", "don't",
             "down",
             "downwards", "during", "each", "edu", "eg", "eight", "eighty", "either", "else", "elsewhere", "end",
             "ending",
             "enough", "entirely", "especially", "et", "etc", "even", "ever", "evermore", "every", "everybody",
             "everyone",
             "everything", "everywhere", "ex", "exactly", "example", "except", "fairly", "far", "farther", "few",
             "fewer",
             "fifth", "first", "five", "followed", "following", "follows", "for", "forever", "former", "formerly",
             "forth",
             "forward", "found", "four", "from", "further", "furthermore", "get", "gets", "getting", "given", "gives",
             "go",
             "goes", "going", "gone", "got", "gotten", "greetings", "had", "hadn't", "half", "happens", "hardly", "has",
             "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "hello", "help", "hence", "her", "here",
             "hereafter", "hereby", "herein", "here's", "hereupon", "hers", "herself", "he's", "hi", "him", "himself",
             "his",
             "hither", "hopefully", "how", "howbeit", "however", "hundred", "i'd", "ie", "if", "ignored", "i'll", "i'm",
             "immediate", "in", "inasmuch", "inc", "inc.", "indeed", "indicate", "indicated", "indicates", "inner",
             "inside",
             "insofar", "instead", "into", "inward", "is", "isn't", "it", "it'd", "it'll", "its", "it's", "itself",
             "i've",
             "just", "k", "keep", "keeps", "kept", "know", "known", "knows", "last", "lately", "later", "latter",
             "latterly",
             "least", "less", "lest", "let", "let's", "like", "liked", "likely", "likewise", "little", "look",
             "looking",
             "looks", "low", "lower", "ltd", "made", "mainly", "make", "makes", "many", "may", "maybe", "mayn't", "me",
             "mean", "meantime", "meanwhile", "merely", "might", "mightn't", "mine", "minus", "miss", "more",
             "moreover",
             "most", "mostly", "mr", "mrs", "much", "must", "mustn't", "my", "myself", "name", "namely", "nd", "near",
             "nearly", "necessary", "need", "needn't", "needs", "neither", "never", "neverf", "neverless",
             "nevertheless",
             "new", "next", "nine", "ninety", "no", "nobody", "non", "none", "nonetheless", "noone", "no-one", "nor",
             "normally", "not", "nothing", "notwithstanding", "novel", "now", "nowhere", "obviously", "of", "off",
             "often",
             "oh", "ok", "okay", "old", "on", "once", "one", "ones", "one's", "only", "onto", "opposite", "or", "other",
             "others", "otherwise", "ought", "oughtn't", "our", "ours", "ourselves", "out", "outside", "over",
             "overall",
             "own", "particular", "particularly", "past", "per", "perhaps", "placed", "please", "plus", "possible",
             "presumably", "probably", "provided", "provides", "que", "quite", "qv", "rather", "rd", "re", "really",
             "reasonably", "recent", "recently", "regarding", "regardless", "regards", "relatively", "respectively",
             "right",
             "round", "said", "same", "saw", "say", "saying", "says", "second", "secondly", "see", "seeing", "seem",
             "seemed",
             "seeming", "seems", "seen", "self", "selves", "sensible", "sent", "serious", "seriously", "seven",
             "several",
             "shall", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "since", "six", "so", "some",
             "somebody", "someday", "somehow", "someone", "something", "sometime", "sometimes", "somewhat", "somewhere",
             "soon", "sorry", "specified", "specify", "specifying", "still", "sub", "such", "sup", "sure", "take",
             "taken",
             "taking", "tell", "tends", "th", "than", "thank", "thanks", "thanx", "that", "that'll", "thats", "that's",
             "that've", "the", "their", "theirs", "them", "themselves", "then", "thence", "there", "thereafter",
             "thereby",
             "there'd", "therefore", "therein", "there'll", "there're", "theres", "there's", "thereupon", "there've",
             "these",
             "they", "they'd", "they'll", "they're", "they've", "thing", "things", "think", "third", "thirty", "this",
             "thorough", "thoroughly", "those", "though", "three", "through", "throughout", "thru", "thus", "till",
             "to",
             "together", "too", "took", "toward", "towards", "tried", "tries", "truly", "try", "trying", "t's", "twice",
             "two", "un", "under", "underneath", "undoing", "unfortunately", "unless", "unlike", "unlikely", "until",
             "unto",
             "up", "upon", "upwards", "us", "use", "used", "useful", "uses", "using", "usually", "v", "value",
             "various",
             "versus", "very", "via", "viz", "vs", "want", "wants", "was", "wasn't", "way", "we", "we'd", "welcome",
             "well",
             "we'll", "went", "were", "we're", "weren't", "we've", "what", "whatever", "what'll", "what's", "what've",
             "when",
             "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "where's", "whereupon",
             "wherever",
             "whether", "which", "whichever", "while", "whilst", "whither", "who", "who'd", "whoever", "whole",
             "who'll",
             "whom", "whomever", "who's", "whose", "why", "will", "willing", "wish", "with", "within", "without",
             "wonder",
             "won't", "would", "wouldn't", "yes", "yet", "you", "you'd", "you'll", "your", "you're", "yours",
             "yourself",
             "yourselves", "you've", "zero"])

    # Naive method for splitting a text into sentences
    def split_content_to_sentences(self, content):
        content = content.replace("\n", ". ")
        splitcontent = content.split(". ")
        return splitcontent

    # Naive method for splitting a text into paragraphs
    def split_content_to_paragraphs(self, content):
        return content.split("\n\n")

    # Caculate the intersection between 2 sentences
    def sentences_intersection(self, sent1, sent2):

    # split the sentence into words/tokens
    #         s1 = set(set(sent1.split(" ")) - self.stopwords)
    #         s2 = set(set(sent2.split(" ")) - self.stopwords)
        s1 = set(sent1.split(" "))
        s2 = set(sent2.split(" "))

        # If there is not intersection, just return 0
        if (len(s1) + len(s2)) == 0:
            return 0

        # We normalize the result by the average number of words
        return len(s1.intersection(s2)) / ((len(s1) + len(s2)) / 2)

    # Format a sentence - remove all non-alphbetic chars from the sentence
    # We'll use the formatted sentence as a key in our sentences dictionary
    def format_sentence(self, sentence):
        sentence = re.sub(r'\W+', ' ', sentence)
        return sentence

    # Convert the content into a dictionary <K, V>
    # k = The formatted sentence
    # V = The rank of the sentence
    def get_senteces_ranks(self, content):

        # Split the content into sentences
        sentences = self.split_content_to_sentences(content)

        # Calculate the intersection of every two sentences
        n = len(sentences)
        values = [[0 for x in xrange(n)] for x in xrange(n)]
        for i in range(0, n):
            for j in range(0, n):
                values[i][j] = self.sentences_intersection(sentences[i], sentences[j])

        # Build the sentences dictionary
        # The score of a sentences is the sum of all its intersection
        sentences_dic = {}
        for i in range(0, n):
            score = 0
            for j in range(0, n):
                if i == j:
                    continue
                score += values[i][j]
            sentences_dic[self.format_sentence(sentences[i])] = [score, i]
        return sentences_dic

    # Return the best sentence in a paragraph
    def get_best_sentence(self, paragraph, sentences_dic):

        # Split the paragraph into sentences
        sentences = self.split_content_to_sentences(paragraph)

        # Ignore short paragraphs
        if len(sentences) < 2:
            return ""

        # Get the best sentence according to the sentences dictionary
        best_sentence = ""
        max_value = 0
        for s in sentences:
            strip_s = self.format_sentence(s)
            if strip_s:
                if sentences_dic[strip_s][0] > max_value:
                    max_value = sentences_dic[strip_s][0]
                    best_sentence = s

        return best_sentence

    # Build the summary
    def get_summary(self, title, content, sentences_dic):

        # Split the content into paragraphs
        paragraphs = self.split_content_to_paragraphs(content)
        print "len(paragraphs):%d" % len(paragraphs)

        # Add the title
        summary = []
        summary.append(title.strip())
        summary.append("")

        # Add the best sentence from each paragraph
        for p in paragraphs:
            sentence = self.get_best_sentence(p, sentences_dic).strip()
            if sentence:
                summary.append(sentence)

        return ("\n").join(summary)


# Main method, just run "python summary_tool.py"
def main():
    
    title = """
    The French Revolution
    """

    content = """In this video we&#39;re going to talk about the French Revolution.
And what makes this especially significant is that not only is this independence from a monarchy-controlled empire, like in the American independence, this is an actual overthrowing of a monarchy.
A monarchy that controls a major world power.
Depending on how you view it, the American Revolution came first and kind of put out the principles of self-governance and why do we need kings and all of that.
But the French Revolution was the first time that those type of principles really took foot in Europe and really overthrow a monarchy.
So just to understand kind of the environment in which this began, let&#39;s talk about what France was like in 1789.
Which most people kind of view as the beginning of the Revolution.
One, France was poor.
Now, you wouldn&#39;t think that France was poor, if you looked at Louis XVI, who was king of France.
If you looked at Louis XVI, and the clothes he wore.
If you looked at Marie-Antoinette, his wife, they don&#39;t look poor.
They lived in the palace of Versailles, which is ginormous.
It&#39;s this massive palace, it would compare to the greatest palaces in the world.
They were living a lavish lifestyle.
Just in case you want to know where this is, this is what&#39;s now almost a suburb of Paris.
But at the time it was a village 20 or 30 kilometers away from Paris.
So they don&#39;t seem to be poor.
But the the actual government of France is poor.
And when I say poor, they&#39;re in debt.
They&#39;ve just had two major military adventures.
One was the American Revolution.
They played a major part in supporting the revolutionaries.
Because they wanted to stick it to their enemy, Great Britain.
They wanted their empire to shrink a little bit.
So France sent significant military help and resources.
And you could imagine, that&#39;s not a cheap thing when you&#39;re doing it across the Atlantic Ocean.
And even before the American Revolution, the Seven Years&#39; War that ended in 1763, this really drained the amount of wealth that the French government had.
And for those of you who are more American history focused, the Seven Years&#39; War is really the same thing as the French and Indian War.
The French and Indian War was the North American theater of the Seven Years&#39; War.
But the Seven Years&#39; War is the more general term.
Because there was also a conflict going on in Europe simultaneously.
The French and Indian War and it was just part of that conflict.
And the Seven Years&#39; actually engulfed most of the powers of Europe at the time.
So France had participated in this, ended in 1763, you had the American Revolution.
Both of these really just drained the amount of funds that the government itself had.
At the same time, the French people were starving.
There was a generalized famine at the time.
They weren&#39;t producing enough grain, people couldn&#39;t get their bread to eat.
So you can imagine, when people are starving they&#39;re not happy.
And to kind of add insult to injury, you would see your royals living like this.
But even worse than the royals, who you don&#39;t see every day, you saw your nobility.
Who is roughly a little over 1.5% of the population.
But you saw the nobility really, really, living it up.
And the nobility, just so you know, these are people with fancy titles who inherit land and wealth from generation to generation.
They don&#39;t dress too differently from the king.
And they essentially live in smaller versions of the palace of Versailles.
And if you&#39;re a peasant, you work on their fields, do all the work, you send them some of your crops and they pay no taxes.
So from your point of view, and it&#39;s not hard to understand why you would think this, these are essentially kind of parasites who are completely ignoring the fact that you are starving and you&#39;re paying all of the taxes.
You can imagine people weren&#39;t too happy about that.
And then to top it all off, you had all of these philosophers hanging around talking about the Enlightenment.
And this is kind of the whole movement where people, and authors, and poets, and philosophers, are starting to realize that, gee, maybe we don&#39;t need kings.
Maybe we don&#39;t need priests to tell us what it means to be good or bad.
Maybe people could essentially rule themselves all of a sudden.
And obviously, the biggest proof of the Enlightenment was the American Revolution.
That was kind of the first example of people rising up and saying, we don&#39;t need these kings anymore.
We want to govern ourselves.
For the people, by the people.
So you also had kind of this philosophical movement going around.
Now if you ask me my opinion of what the biggest thing was, I think the people starving, you can never underestimate what people are willing to do when they&#39;re actually hungry.
And, this is kind of more from the intellectual point of view.
People said, oh there&#39;s Enlightenment movement here.
So this is the state of France.
They had a financial crisis.
So a meeting was called, kind of an emergency meeting, of the major groups of France to try to resolve some of these problems.
It&#39;s a fiscal crisis, people are starving, what do you do?
So they called the Convocation of the Estates-General.
Let me write that down.
Which was a meeting of the three estates of France.
Now what are the three estates of France?
You can really just view them as the three major social classes of France.
The First Estate was the clergy.
The Second Estate is the nobility.
And then the Third Estate is everyone else.
And this gives you a sense of how skewed the power structure was.
Because people kind of grouped the power as OK, these are the three groups and maybe they can vote against each other.
But this was only 0.5% of the population, this is 1.5% of the population, this was 98% of the population.
But these people had equal weight with these guys.
But these people had the burden of most of the taxes.
These are the people who are doing all the work, producing all of France&#39;s wealth, dying in the wars.
But these guys, despite their small population, have more weight than everybody else.
So you had the Convocation of the Estates-General, where representatives of these three estates met at the Palace of Versailles to especially figure out what to do about this fiscal crisis.
Now obviously, these people right here, the Third Estate, they were angry.
They were like look, we&#39;ve taken the burden on ourselves for much of the recent history of France.
We&#39;re tired of you guys getting away with not paying taxes and just kind of leeching off of us.
They were afraid that even more of the tax burden was going to be put on them.
And the nobility, or the king, or the clergy, that they wouldn&#39;t have to make sacrifices.
So they came in already angry.
And so they really wanted to meet in one big room together.
Because they actually had roughly 600 representatives.
Which only the king at the last minute agreed to.
Before, it was only going to be equal numbers of them.
These guys had 300 roughly.
These guys had 300 as well.
These guys were able to say, hey we&#39;re 98% of the population, maybe we should have at least 600 representative.
But even there, they wanted to meet in the same room.
And essentially try to make it so it&#39;s one representative, one vote.
But obviously these other estates, the clergy and the nobility, said no, let&#39;s each vote as estates.
And at the end of the day, these guys lost.
So they were essentially forced to kind of organize independently as a Third Estate.
So that made them even angrier.
So they met at an assembly hall and said, if these guys are going to ignore us, not only are we going to be in this room and start organizing ourselves.
But we&#39;re not going to call this the Convocation of the Estates-General.
We&#39;re going to declare that we are the National Assembly of France.
That we represent the people.
We are essentially going to become the parliamentary body of France.
Instead of just being this emergency Convocation of the Estates-General.
And they actually got some sympathy from some elements of the clergy and some elements of the nobility.
Now obviously, Louis XVI was not amused by this whole turn of events.
Here he was, he was an absolute monarch, which means that he held pretty much all of the power to do whatever he saw was fit.
And all of a sudden you had this group of upstarts taking advantage of this emergency situation where he can&#39;t continue to buy as many silk robes as he was before.
They&#39;re taking advantage of the situation to declare a National Assembly of France.
To declare somehow that I&#39;m not an absolute monarch.
That my power is going to be taken by this assembly.
So he wasn&#39;t happy.
So when they took a break, he locked the door of the assembly room.
So they couldn&#39;t get in.
And he said, oh I think there needs to be some repairs in that room.
Maybe you all can assemble later.
And that was kind of his way of saying no.
If you&#39;re declaring you&#39;re the National Assembly of France, I&#39;m not going to even let you assemble.
I&#39;m not even going to let you get in the room.
So that clearly didn&#39;t do a lot to make these guys, or in particular these guys, any happier.
People are hungry.
These people are living lavishly.
They&#39;ve already been not allowed to vote in one room together.
When they vote in their own room, and declare themselves as representatives of the people of France, which they really are, the king locks the room, doesn&#39;t let them go in.
So they go to an indoor tennis court in Versailles.
This is a picture of it right here.
This is an indoor tennis court.
And that gives you an idea of how lavish Versailles was, that it had an indoor tennis court in the late 1700s.
And they proclaimed the Tennis Court Oath.
Where they proclaimed, not are we only the National Assembly of France, but even more than that, we all pledge to not stop until we create a constitution of France.
So they went from being a National Assembly to essentially morphing into a constituent assembly.
We&#39;re going to create a constitution.
And they had sympathy from some elements of the clergy and the nobility.
So eventually Louis XVI, he kind of saw the writing on the wall.
The people are angry.
And every time he tries to mess with them, they only get angrier.
And they only go to even more extreme measures.
So just to kind of make it seem like he&#39;s going along, he says, OK that&#39;s cool, guys.
Whatever you all want to do.
Yeah, maybe I&#39;m open to it, we are in an emergency.
And maybe it is unreasonable, I have been a little bit unreasonable.
So he lets them be, he lets them assemble again.
But while that&#39;s happening, people start to notice that troops are converging on Paris.
And they&#39;re obviously being sent there by the king.
And not only are they just any troops, a lot of the actual troops, even though they are French troops, there under the authority of France&#39;s military.
They&#39;re actually foreign troops.
So, if you think about it, these would be the ideal types of troops to put down any type of insurgency, or any type of rebellion.
Or even better, to go in and dissolve the National Assembly.
So people start getting a little bit paranoid, you can imagine.
Now on top of that, Louis XVI&#39;s main financial adviser, Necker, Jacques Necker.
He was sympathetic to the Third Estate, to the plight of the Third Estate.
And he said hey, Mr. King, I think it&#39;s reasonable for you to essentially budget your expenses a little bit better.
And maybe a little bit less of a lavish lifestyle.
Considering the state of the government&#39;s budget.
And the state of the people of France, they&#39;re starving.
Why don&#39;t you do that a little bit?
But Louis XVI, instead of taking his advice, he fired him.
He fired the financial adviser.
So taken together, troops are converging on Paris, you have this Tennis Court Oath, Louis XVI has fired his adviser, people are going hungry.
They&#39;re genuinely going hungry.
People in Paris said, the king is going to try to suppress us again, this is no good.
And especially if he does it with troops, we have to arm ourselves.
So they stormed the Bastille.
This right here is a picture of the Bastille.
And this is most famous, when you when you first learn about it, or maybe this is the first time you&#39;re learning about it.
They put political prisoners there and they freed the political prisoners.
But in reality, there were only seven prisoners in the Bastille.
So it&#39;s not like thousands and thousands of political prisoners were being held there and there were freed.
The real value of the Bastille to the revolutionaries, we could say, is that there were weapons there.
There was a major arms cache there.
And so by storming the Bastille and getting the weapons, they all of a sudden could essentially fend off any type of threat that the troops would have.
But this is also kind of the very beginning of the real chaos of the French Revolution.
And as we&#39;re going to see over the next several years, the chaos only gets worse and worse.
It&#39;s almost on a lot of levels a lot worse than the American Revolution.
Because what actually happened in the cities and what fellow Frenchman started doing to do each other was really on many levels barbaric.
And you actually saw it here for the first time, where the governor of the Bastille, the guy who was in charge of it, he had the standoff between the troops.
And he eventually called for a ceasefire.
Because he&#39;s like, oh there&#39;s too much bloodshed.
But once the revolutionaries got to him, they stabbed them, they cut his head off, and they put it on a pike.
Then they went back to the mayor of Paris, they shot him.
So clearly, things were really getting out of hand.
But most people associate the storming of the Bastille as kind of the landmark event of the French Revolution.
Even today, people celebrate Bastille Day.
And that is July 14, 1798.
So just to give you a sense of how quickly all of this happened, the Convocation of the Estates-General, that was in May.
The Tennis Court Oath was in June.
And then in July, you have the storming of the Bastille.
And then in August, just to kind of complete the idea that we are definitely in a revolutionary period.
The National Assembly, that started off at the tennis courts with the Third Estate, they declared their equivalent of the Declaration of Independence.
They declared their Declaration of the Rights of Man and of the Citizen.
Which was essentially their version of the Declaration of Independence.
And it essentially put everything into question of what is life, liberty, and the pursuit of happiness?
I&#39;m using words from the American Revolution.
But this was their Declaration of Independence.
It wasn&#39;t a constitution, it was just a statement of the things that they think need to govern any type of constitution or country.
Or the ideas that any country should be based on.
So I&#39;m going to leave you there.
We&#39;ve really now started the French Revolution.
And now, you&#39;re going to see that over the next several years, it&#39;s only going to get bloodier and bloodier and even more complex.
And when everything is said and done, it&#39;s actually not going to end that well in terms of giving people liberty."""

    # Create a SummaryTool object
    st = SummaryTool()

    # Build the sentences dictionary
    sentences_dic = st.get_senteces_ranks(content)
    print len(sentences_dic)

    # Get top N sentences by rank
    top_sentences = []
    for item in sorted(sentences_dic.items(), key=lambda (k, v): (v, k), reverse=True)[0:20]:
        sentence = item[0]
        score, position = item[1]
        top_sentences.append([sentence, score, position])

    for sentence in sorted(top_sentences, key=operator.itemgetter(2)):
        print sentence

    # Build the summary with the sentences dictionary
    summary = st.get_summary(title, content, sentences_dic)

    # Print the summary
    #print summary

    # Print the ratio between the summary length and the original length
    print ""
    print "Original Length %s" % (len(title) + len(content))
    print "Summary Length %s" % len(summary)
    print "Summary Ratio: %s" % (100 - (100 * (len(summary) / (len(title) + len(content)))))


if __name__ == '__main__':
    main()