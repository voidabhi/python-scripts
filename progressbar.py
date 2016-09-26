################################################################################
# Example usage:
# $ python
# >>> import Progress
# >>> total = 100
# >>> message = 'Doing this task '
# >>> with Progress.Bar(total, message) as bar:
# ...     for n in range(total):
# ...         time.sleep(0.1)
# ...         bar.update()
# ...
# Doing this task [------------------------------------------------------------]
################################################################################
import sys
################################################################################
class Bar:

    # A progress bar is draw using 4 elements:
    # 1. A message
    # 2. The left (start) boundary
    # 3. The body of the progress bar
    # 4. The right (end) boundary
    template = '{msg}{start}{body}{end}'

##################################################

    def __init__(self, total, message='', max_width=80,
                 marker='#', placeholders='-',
                 start='[', end=']'):

        # Assume zero width so that self.from_template() works
        self.width = 0

        # A bar measures progress towards a total
        self.total = total

        # A progress bar may have a message before it
        self.message = message

        # A Progress.Bar is a series of markers
        self.marker = marker

        # drawn over the top of placeholders
        self.placeholders = placeholders

        # and delimited by start and end characters
        self.start=start
        self.end=end

        # calculate how much of the max_width will be consumed by the message
        # and the start/end delimiters.
        padding_width = len(self.from_template())

        # Calculate the width of the body of the bar
        self.width = max_width - padding_width

        # How many parts of the total go per marker in the body of the bar
        self.granularity = total / self.width

##############################

    def from_template(self):
        ''' Returns a string representation of the Progress.Bar, including the
            message, the start and end markers and a series of placeholders.
        '''
        return self.template.format(msg = self.message,
                                    start = self.start,
                                    end = self.end,
                                    body = self.placeholders * self.width)

##################################################

    def __enter__(self):
        # How much of the total has passed
        self.progress = 0

        # How much of the width has been drawn
        self.rendered = 0

        # Write out the Progress.Bar with placeholders
        sys.stdout.write(self.from_template())

        # Write out backspaces until the cursor is at the start marker
        sys.stdout.write('\b' * (self.width + len(self.end)))
        sys.stdout.flush()

        # act as a proper generator
        return self

##############################

    def __exit__(self, type, value, traceback):
        # always render a completed Progress.Bar
        while not self.is_fully_rendered():
            self.render()

        # then finish on the next line
        print('')

##################################################

    def render(self):
        ''' Outputs one marker over the top of a placeholder if the progress
            bar is still not fully rendered.
        '''
        self.rendered += 1
        if not self.is_fully_rendered():
            sys.stdout.write(self.marker)
            sys.stdout.flush()

##############################

    def is_fully_rendered(self):
        return self.rendered > self.width

##################################################

    def update(self, n=1):
        ''' Update the Progress.Bar n counts towards the total.
        '''
        if n > 0:
            self.progress += 1
            while self.progress / self.granularity > self.rendered:
                self.render()
            self.update(n-1)
