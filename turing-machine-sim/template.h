#ifndef TM_NODE
#define TM_NODE

#include <strings.h>
#include <stdbool.h>

typedef struct tm_node {
    int value;
    tm_node *prev;
    tm_node *next;
} tm_node;

#define TAPE_RIGHT 1
#define TAPE_LEFT (1 << 1)
#define DO_WRITE  (1 << 2)

typedef struct tm_cmd {
    int value;
    tm_state *next;
    char opts;
} tm_cmd;

#define ACCEPT_STATE 1
#define REJECT_STATE 2
typedef struct tm_state {
    tm_cmd *transitions;
    bool flags;
} tm_state;

// returns true on success
bool starting_tape(char *input, int dflt, tm_node *buffer, size_t bufflen)
{
    size_t slen = strlen(input);
    if (slen > bufflen) {
        return false;
    }

    int i;
    tm_node *prev = NULL;

    for(i = 0; i < slen; i++) {
        tm_node newnode;
	newnode.prev = prev;
	newnode.next = NULL;
	newnode.value = input[i];
	*(buffer + i) = newnode;
	
	if(prev != NULL) {
            prev->next = newnode;
	}

	prev = newnode;
    }
    for(; i < bufflen; i++) {
        tm_node newnode;
	newnode.prev = prev;
	newnode.next = NULL;
	newnode.value = dflt;
        *(buffer + i) = newnode;
	if(prev != NULL) {
	    prev->next = newnode;
	}
	prev = newnode;
    }

    return true;
}

// returns new head
tm_node* tape_left(tm_node *n, tm_node *buff, bool *buff_used)
{
    if(n->prev != NULL) {
        *buff_used = false;
	return n->prev;
    }

    *buff_used = true;
    n->prev = buff;
    return buff;
}

tm_node *tape_right(tm_node *n, tm_node *buff, bool *buff_used)
{
    if(n->next != NULL) {
        *buff_used = false;
	return n->next;
    }

    *buff_used = true;
    n->next = buff;
    return buff;
}

bool run_machine(tm_node *n, tm_state *init_state)
{
    tm_node b;
    tm_node *buffer = &b;
    bool buff_used = false;

    while(!(init_state->flags & (ACCEPT_STATE | REJECT_STATE))) {
        int node_value = n->value;
        tm_cmd cmd = init_state->transitions[node_value];
	if(cmd & DO_WRITE)
            n->value = cmd.value;
	if(cmd & TAPE_RIGHT) {
            n = tape_right(n, buffer, &buff_used);
	    if(buff_used)
                buffer = (tm_node*)malloc(sizeof(b));
	}
	else if(cmd & TAPE_LEFT) {
	    n = tape_left(n, buffer, &buff_used);
	    if(buff_used)
                buffer = (tm_node*)malloc(sizeof(b));
	}
	init_state = cmd.next;
    }

    return init_state->flags & ACCEPT_STATE;
}

void write_tape_to_file(tm_node *n, int lindex, int rindex, 
		        FILE *fp, char *trans_table)
{
    fprintf(fp, "%d:\n", index);
    while(lindex++ < rindex && n != NULL) {
        fprintf(fp, "%c", trans_table[n->value]);
        n = n->next;
    }
}

tm_node *read_tape_from_file(FILE *fin, char *translation_table)
{
}
#endif

#ifdef EXAMPLE
int main(void)
{
    tm_node buffer[100];
    tm_node *n = starting_tape("10", buffer, 100);

    tm_state qAccept;
    tm_state qOdd;
    tm_state qEven;
    tm_state qReject;

    qAccept.flags = ACCEPT_STATE;
    qReject.flags = REJECT_STATE;
    qOdd.flags = 0;
    qEven.flags = 0;
}
#endif /* EXAMPLE */
